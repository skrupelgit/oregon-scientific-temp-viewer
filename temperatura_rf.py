import postgresql
from subprocess import Popen, PIPE, STDOUT
import sys
import json
from datetime import datetime
from datetime import timedelta
import Adafruit_DHT
import time
import logging

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 3

logging.basicConfig(filename='/home/pi/django/error.log',level=logging.WARNING)

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
    global db, channelsId, logging
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
        time.sleep(10)


cmd = "/home/pi/django/temperaturas_rf/oregonPi"


## run it ##
p = Popen(cmd, stdout=PIPE,
          stderr=STDOUT)


while True:
    if channelsId[str(0)]['seen'] + timedelta(minutes = 5) <= datetime.now():

        try:
            humidity, temperature=Adafruit_DHT.read_retry(
                DHT_SENSOR, DHT_PIN, retries = 3, delay_seconds = 1)
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

    try:
        line=p.stdout.readline()
    except:
        print("excepcion leyendo test")
        logging.warning('Error leyendo test')
        p=Popen(cmd, stdout = PIPE,
                      stderr = STDOUT)
        logging.warning('test reinicializado')
        

    if not line:
        continue
    else:
        try:
            temp=json.loads(line)

            if temp['channel'] == -1:
                continue
            if channelsId[str(temp['channel'])]['seen']+timedelta(minutes = 5) <= datetime.now():
                persistInDb(temp)
        except:
            print("excepcion ultimo bloque")
            logging.warning('excepcion ultimo bloque'+ line)

            continue
