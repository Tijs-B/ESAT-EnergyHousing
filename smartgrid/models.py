from django.db import models
from numpy import *

# Create your models here.


class Neighbourhood(models.Model):
    energy_price = models.FloatField()


class House(models.Model):
    neighbourhood = models.ForeignKey("Neighbourhood")


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

<<<<<<< HEAD
=======

### Sensor ###
class Sensor(models.Model):
    house = models.ForeignKey("House")
    type = models.TextField


class Recording(models.Model):
    sensor = models.ForeignKey("Sensor")
    value = models.FloatField()
    timestamp = models.DateTimeField()

>>>>>>> origin/master
