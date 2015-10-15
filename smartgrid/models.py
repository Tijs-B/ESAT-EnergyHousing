from django.db import models

# Create your models here.

class Neighbourhood(models.Model):
    energy_price = models.FloatField()


class House(models.Model):
    neighbourhood = models.ForeignKey(Neighbourhood)


class Room(models.Model):
    house = models.ForeignKey(House)


class Appliance(models.Model):
    room = models.ForeignKey(Room)
    priority = models.IntegerField()
class Heatload(models.Model):
     appliance = models.ForeignKey(Appliance)
class Variablepower(models.Model):
    heatload = models.ForeignKey(Heatload)
    VeryCold = 'T<-10'
    Cold = 'T<0'
    Normal = '0<T<20'
    Hot = 'T>20'
    temppossibilities = ((VeryCold,'T<-10'),(Cold, 'T<0'),( Normal, '0<T<20'),(Hot,'T>20'))
    temprange = models.CharField(max_length=10,choices=temppossibilities,default=Cold)
    VeryLow = '1-50'
    Low = '50-100'
    Medium = '100-200'
    High = '200-500'
    VeryHigh = '500-1000'
    powerpossibilities = ((VeryLow,'1-50'),(Low,'50-100'),(Medium,'100-200'),(High,'200-500'),(VeryHigh,'500-100'))
    powerrange = models.CharField(max_length=10,choices=powerpossibilities,default=Medium)

### Sensor ###
class Sensor(models.Model):
    house = models.ForeignKey(House)
    type = models.TextField


class Recording(models.Model):
    sensor = models.ForeignKey(Sensor)
    value = models.FloatField()
    timestamp = models.DateTimeField()

