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
