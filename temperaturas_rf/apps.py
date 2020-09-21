from django.apps import AppConfig
import postgresql
from subprocess import Popen, PIPE, STDOUT
import sys
import json
from datetime import datetime
from datetime import timedelta
import Adafruit_DHT
import time
import logging
import threading
import os
from oslo_concurrency import lockutils
from oslo_concurrency import processutils

myapp_synchronized = lockutils.synchronized_with_prefix("/home/pi/django")
lockutils.set_defaults(lock_path="/tmp/tmpbFHKE45")


class TemperaturasRfConfig(AppConfig):
    name = 'temperaturas_rf'
    verbose_name = "Tempperaturas Radio Frecuencias"
    db = postgresql.open('pq://alex:2123qQ@localhost/casa')
    myapp_synchronized = lockutils.synchronized_with_prefix("myapp")

    channelsId = {
        "2": {
            "id": 2,
            "seen": datetime.now() - timedelta(minutes=5)
        },
        "3": {
            "id": 3,
            "seen": datetime.now() - timedelta(minutes=5)
        },
        "1": {
            "id": 4,
            "seen": datetime.now() - timedelta(minutes=5)
        },
        "0": {
            "id": 5,
            "seen": datetime.now() - timedelta(minutes=5)
        }
    }

    def persistInDb(self, temp):
        try:
            prepareTemp = self.db.prepare(
                "INSERT INTO  temperaturas_rf_temperature (temp, humidity, sensor_id, date) VALUES ($1, $2, $3, NOW())")
            prepareTemp(
                temp['temp'],
                temp['humidity'],
                self.channelsId[str(temp['channel'])]['id']
            )

            
            prepareSensor = self.db.prepare(
                "UPDATE temperaturas_rf_sensor SET  battery_low=$1, last_updated=NOW() where channel=$2")
            prepareSensor(temp['low_battery'], str(temp['channel']))
            self.channelsId[str(temp['channel'])]['seen'] = datetime.now()
        except:
            logging.warning("excepcion sql")
            logging.warning(temp)
        finally:
            time.sleep(10)

    def ready(self):
        logging.basicConfig(
            filename='/home/pi/django/error.log', level=logging.INFO)
        
        logging.info("Funcion ready PID:"+str(os.getpid()))    

        t = threading.Thread(target=self.startMeasuring, args=(), kwargs={})
        t.setDaemon(True)
        t.start()

    @myapp_synchronized('not_thread_process_safe', external=True)
    def startMeasuring(self):

        logging.basicConfig(
            filename='/home/pi/django/error.log', level=logging.INFO)



        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = 3

    

        logging.info('inicio del daemon en el proceso '+str(os.getpid())+' en '+ os.getcwd())
   


        cmd = "./test"

        ## run it ##
        p = Popen(cmd, stdout=PIPE,
                  stderr=STDOUT)

        while True:
            if self.channelsId[str(0)]['seen'] + timedelta(minutes=5) <= datetime.now():

                try:
                    humidity, temperature = Adafruit_DHT.read_retry(
                        DHT_SENSOR, DHT_PIN, retries=3, delay_seconds=1)
                    if humidity is not None and temperature is not None:
                        self.persistInDb({
                            "temp": temperature,
                            "humidity": humidity,
                            "channel": 0,
                            "low_battery": 0
                        })
                except:
                    logging.warning('Error primer bloque')
                    print("excepcion primer bloque")

            try:
                line = p.stdout.readline()
            except:
                print("excepcion leyendo test")
                logging.warning('Error leyendo test')
                p = Popen(cmd, stdout=PIPE,
                          stderr=STDOUT)
                logging.warning('test reinicializado')

            if not line:
                continue
            else:
                try:
                    temp = json.loads(line)

                    if temp['channel'] == -1:
                        continue
                    if self.channelsId[str(temp['channel'])]['seen']+timedelta(minutes=5) <= datetime.now():
                        self.persistInDb(temp)
                except:
                    print("excepcion ultimo bloque")
                    logging.warning('excepcion ultimo bloque' + line)

                    continue
