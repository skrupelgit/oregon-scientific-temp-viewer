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

    myapp_synchronized = lockutils.synchronized_with_prefix("myapp")

    def ready(self):
        logging.basicConfig(
            filename='/home/pi/django/error.log', level=logging.INFO)

        logging.info("Funcion ready PID:"+str(os.getpid()))    
        t = threading.Thread(target=self.startMeasuring, args=(), kwargs={})
        t.start()


    @myapp_synchronized('not_thread_process_safe', external=True)
    def startMeasuring(self):
        logging.info("Lanzamos proceso measuring PID:"+str(os.getpid()))    
        Popen("/usr/bin/python3 ./measuring.py", stdout=PIPE,
                  stderr=STDOUT)

      
            