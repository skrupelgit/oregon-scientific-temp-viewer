#!/usr/bin/python
from subprocess import Popen, PIPE, STDOUT
import sys
import json
from models.Sensor import Sensor

## command to run - tcp only ##
cmd = "./test"
 



## run it ##
p = Popen(cmd, shell=True, stdout = PIPE, 
        stderr = STDOUT)
print("-----------INICIO-----------")
 
## But do not wait till netstat finish, start displaying output immediately ##
while True:
    line = p.stdout.readline()
    if not line: break
    else:
        temp=json.loads(line)
