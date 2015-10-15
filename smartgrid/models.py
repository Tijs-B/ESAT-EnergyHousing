from django.db import models
from numpy import *

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

    class FixedDemand(models.Model):
        consumption = models.FloatField()
        active = models.BooleanField()

    class ShiftingLoadCycle(models.Model):
        due = models.DateTimeField('Tot: ')

        def consumption_profile(self, length, power):
            """
            Returns a 2*len(length) matrix. In the first column you find the time
            in the second column, you find the power at that time.
            """
            profile = zeros(shape=(len(length), 2))
            index = 0
            for t in length:
                profile[index][0] = length[t]
                profile[index][1] = power[t]
                index += 1
            return profile



