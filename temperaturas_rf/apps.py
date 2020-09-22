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

class TemperaturasRfConfig(AppConfig):
    name = 'temperaturas_rf'
    verbose_name = "Tempperaturas Radio Frecuencias"


    def ready(self):
        logging.basicConfig(
            filename='/home/pi/django/error.log', level=logging.INFO)


            