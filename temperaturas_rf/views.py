from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Sensor, Temperature
from django.forms.models import model_to_dict
from django.core import serializers
import json
import datetime

def index(request):

     sensors = Sensor.objects.all()
     tempDic={}

     for sensor in sensors:
          tempDic["channel"+sensor.channel]=Temperature.objects.filter(sensor=sensor).order_by('-date')[:5]

     return render(request,"hola.html", tempDic)

def fetchTemperatures(request):
     sensors = Sensor.objects.order_by('channel').all()
     tempDic={}

     for sensor in sensors:
          tempDic["channel"+sensor.channel]={} 
          tempDic["channel"+sensor.channel]['sensorData']= {
               "channel": sensor.channel,
               "name": sensor.name,
               "battery_low": sensor.battery_low,
               "last_updated": sensor.last_updated
          }
          today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
          today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
          tempDic["channel"+sensor.channel]['temperatures']= list(Temperature.objects.filter(sensor=sensor,  date__range=(today_min, today_max)).order_by('-date').values()[:288])

     return JsonResponse(tempDic)

