from django.db import models
from numpy import *

# Create your models here.


class Neighborhood(models.Model):
    def __str__(self):
        return self.neighborhood_name
    energy_price = models.FloatField()
    neighborhood_name = models.CharField(max_length=200)


class House(models.Model):
    neighbourhood = models.ForeignKey("Neighborhood")


class Room(models.Model):
    house = models.ForeignKey("House")


class Appliance(models.Model):

    room = models.ForeignKey("Room")
    priority = models.IntegerField(default=0, choices=(
        (0, 'Low'),
        (1, 'Normal'),
        (2, 'High'),
        (3, 'Very High'))
    )


### Sensor ###
class Sensor(models.Model):
    house = models.ForeignKey("House")
    type = models.TextField


class Recording(models.Model):
    sensor = models.ForeignKey("Sensor")
    value = models.FloatField()
    timestamp = models.DateTimeField()

class Heatload(models.Model):
     appliance = models.ForeignKey(Appliance)


class Variablepower(models.Model):
    heatload = models.ForeignKey(Heatload)
    VeryCold = 'VC'
    Cold = 'C'
    Normal = 'N'
    Hot = 'H'
    temppossibilities = ((VeryCold,'T<-10'),(Cold, 'T<0'),( Normal, '0<T<20'),(Hot,'T>20'))
    temprange = models.CharField(max_length=2,choices=temppossibilities,default=Cold)
    VeryLow = 'VL'
    Low = 'L'
    Medium = 'M'
    High = 'H'
    VeryHigh = 'VH'
    powerpossibilities = ((VeryLow,'1-50'),(Low,'50-100'),(Medium,'100-200'),(High,'200-500'),(VeryHigh,'500-1000'))
    powerrange = models.CharField(max_length=2,choices=powerpossibilities,default=Medium)


class Ivariablepower(models.Model):
    heatload = models.ForeignKey(Heatload)
    VeryCold = 'VC'
    Cold = 'C'
    Normal = 'N'
    Hot = 'H'
    temppossibilities = ((VeryCold,'T<-10'),(Cold, 'T<0'),( Normal, '0<T<20'),(Hot,'T>20'))
    temprange = models.CharField(max_length=2,choices=temppossibilities,default=Cold)
    VeryLow = 'VL'
    Low = 'L'
    Medium = 'M'
    High = 'H'
    VeryHigh = 'VH'
    powerpossibilities = ((VeryLow,'50'),(Low,'100'),(Medium,'200'),(High,'500'),(VeryHigh,'1000'))
    powerrange = models.CharField(max_length=2,choices=powerpossibilities,default=Medium)
