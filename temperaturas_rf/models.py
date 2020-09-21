from django.db import models


class Sensor(models.Model):
    name = models.CharField( max_length=50)
    channel = models.CharField( max_length=50, unique=True)
    battery_low = models.IntegerField()
    last_updated = models.DateTimeField( auto_now_add=False)

    class Meta:
        def __str__(self):
          return self.name



# Create your models here.
class Temperature(models.Model):

    temp = models.FloatField()
    humidity = models.FloatField()
    date = models.DateTimeField( auto_now_add=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    
    class Meta:
        def __str__(self):
            return self.temp

