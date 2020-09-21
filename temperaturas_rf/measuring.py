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

db = postgresql.open('pq://alex:2123qQ@localhost/casa')
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




def persistInDb(temp):
    try:
        prepareTemp = db.prepare(
                "INSERT INTO  temperaturas_rf_temperature (temp, humidity, sensor_id, date) VALUES ($1, $2, $3, NOW())")
        prepareTemp(
                temp['temp'],
                temp['humidity'],
                channelsId[str(temp['channel'])]['id']
            )

            
        prepareSensor = db.prepare(
                "UPDATE temperaturas_rf_sensor SET  battery_low=$1, last_updated=NOW() where channel=$2")
        prepareSensor(temp['low_battery'], str(temp['channel']))
        channelsId[str(temp['channel'])]['seen'] = datetime.now()
    except:
        logging.warning("excepcion sql")
        logging.warning(temp)
    finally:
        pass
            #time.sleep(10)

def startMeasuringRf():
    logging.basicConfig(
            filename='/home/pi/django/error.log', level=logging.INFO)
    logging.info('inicio del daemon en el proceso medidor temperatura Radio frecuencia '+str(os.getpid())+' en '+ os.getcwd())
    cmd = "./test"
    p = Popen(cmd, stdout=PIPE,
                  stderr=STDOUT)
    while True:
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
                if channelsId[str(temp['channel'])]['seen']+timedelta(minutes=5) <= datetime.now():
                    logging.info('Encontrado RF')
                    persistInDb(temp)
            except:
                logging.warning('excepcion ultimo bloque' + line)
                continue


def startMeasuring():
    logging.basicConfig(
            filename='/home/pi/django/error.log', level=logging.INFO)

    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 3

    logging.info('inicio del daemon en el proceso medidor temperatura '+str(os.getpid())+' en '+ os.getcwd())

    while True:
        if channelsId[str(0)]['seen'] + timedelta(minutes=5) <= datetime.now():

            try:
                humidity, temperature = Adafruit_DHT.read_retry(
                    DHT_SENSOR, DHT_PIN, retries=3, delay_seconds=0)
                if humidity is not None and temperature is not None:
                    persistInDb({
                            "temp": temperature,
                            "humidity": humidity,
                            "channel": 0,
                            "low_battery": 0
                        })
            except:
                logging.warning('Error primer bloque')
                print("excepcion primer bloque")


def daemonize():
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #1 failed: {0}\n'.format(err))
        sys.exit(1)
    # decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)
    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #2 failed: {0}\n'.format(err))
        sys.exit(1)
    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(os.devnull, 'w')
    se = open(os.devnull, 'w')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    return True

daemonize()
t = threading.Thread(target=startMeasuringRf, args=(), kwargs={})
t.setDaemon(True)
t.start()
t2 = threading.Thread(target=startMeasuring, args=(), kwargs={})
t2.setDaemon(True)
t2.start()