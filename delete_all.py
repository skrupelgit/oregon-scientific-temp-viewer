import postgresql
from subprocess import Popen, PIPE, STDOUT
import sys
import json
from datetime import datetime  
from datetime import timedelta  

db = postgresql.open('pq://alex:2123qQ@localhost/casa')
channelsId={
    "2":{
        "id":2,
        "seen":None
    },
    "3":{
        "id":3,
        "seen":None
    },
    "1":{
        "id":4,
        "seen":None
    },
    "0":{
        "id":5,
        "seen":None
    }
}

prepareTemp= db.execute("UPDATE temperaturas_rf_sensor set name='Salón' where channel = '0' ")
