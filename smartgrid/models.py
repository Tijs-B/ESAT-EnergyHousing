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
