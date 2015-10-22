from django.db import models


class Neighborhood(models.Model):
    def __str__(self):
        return self.neighborhood_name
    neighborhood_name = models.CharField(max_length=200)
    energy_price = models.FloatField(default=1)


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
    def __str__(self):
        return self.appliance_name
    room = models.ForeignKey("Room")
    appliance_name = models.CharField(max_length=200)
    priority = models.IntegerField(default=0, choices=(
        (0, 'Low'),
        (1, 'Normal'),
        (2, 'High'),
        (3, 'Very High'))
    )
    currently_on = models.BooleanField(default=False)

    # with 'abstract = True', there is no database entry for Appliance, but there will be database entries for classes
    #   that inherit from this class (such as FixedDemand)
    class Meta:
        abstract = True


class FixedDemand(Appliance):
    consumption = models.FloatField()


class ShiftingLoadCycle(Appliance):
    flexibility_start = models.TimeField()
    flexibility_end = models.TimeField()
    time_of_cycle = models.DateTimeField()
    car_min_charge = models.FloatField()
    car_current_charge = models.FloatField()


class HeatLoadVariablePower(Appliance):
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    power_min = models.FloatField()
    power_max = models.FloatField()
    outside_temperature = models.FloatField()


class HeatLoadInvariablePower(Appliance):
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()
    power = models.FloatField()


class ConsumptionProfile(models.Model):
    def __str__(self):
        return self.order
    appliance = models.ForeignKey("ShiftingLoadCycle")
    order = models.IntegerField()
    duration = models.TimeField()
    consumption = models.FloatField()
    # TODO: Consumption profile table


### Sensor ###
class Sensor(models.Model):
    def __str__(self):
        return self.sensor_name
    sensor_name = models.CharField(max_length=200)
    house = models.ForeignKey("House")
    # type = models.TextField


class Recording(models.Model):
    sensor = models.ForeignKey("Sensor")
    value = models.FloatField()
    timestamp = models.DateTimeField()
