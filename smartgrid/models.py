from django.db import models
from numpy import *


class Neighborhood(models.Model):
    def __str__(self):
        return self.neighborhood_name

    energy_price = models.FloatField(default=1)
    neighborhood_name = models.CharField(max_length=200)
class AvailableEnergy(models.Model):
    neighborhood = models.ForeignKey("Neighborhood")
    solar = models.FloatField(default=0)
    wind = models.FloatField(default=0)
    other = models.FloatField(default=0)

class House(models.Model):
    def __str__(self):
        return self.house_name
    neighbourhood = models.ForeignKey("Neighborhood")
    house_name = models.CharField(max_length=200)


class Room(models.Model):
    def __str__(self):
        return self.room_name
    house = models.ForeignKey("House")
    room_name = models.CharField(max_length=200)


### Appliance ###
class Appliance(models.Model):
<<<<<<< HEAD
    # room = models.ForeignKey("Room")
=======
    def __str__(self):
        return self.appliance_name
    room = models.ForeignKey("Room")
    appliance_name = models.CharField(max_length=200)
>>>>>>> refs/remotes/origin/master
    priority = models.IntegerField(default=0, choices=(
        (0, 'Low'),
        (1, 'Normal'),
        (2, 'High'),
        (3, 'Very High'))
    )

<<<<<<< HEAD
    class FixedDemand(models.Model):
        consumption = models.FloatField()
        active = models.BooleanField()
=======
    # with 'abstract = True', there is no database entry for Appliance, but there will be database entries for classes
    #   that inherit from this class.
    class Meta:
        abstract = True


class FixedDemand(models.Model):
    pass


class HeatloadVariablePower(Appliance):
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    power_min = models.FloatField()
    power_max = models.FloatField()


class HeatLoadInvariablePower(Appliance):
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    power = models.FloatField()

>>>>>>> refs/remotes/origin/master

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


#   Sensor   #
class Sensor(models.Model):
    house = models.ForeignKey("House")
    type = models.TextField


class Recording(models.Model):
    sensor = models.ForeignKey("Sensor")
    value = models.FloatField()
    timestamp = models.DateTimeField()
<<<<<<< HEAD

=======
>>>>>>> refs/remotes/origin/master
