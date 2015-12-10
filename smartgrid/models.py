from django.db import models
from django import forms


class Scenario(models.Model):
    scenario_name = models.CharField(max_length=200)
    current_neighborhood = models.CharField(max_length=200)
    time = models.IntegerField(default=1)
    started = models.BooleanField(default=False)
    

class Neighborhood(models.Model):
    def __str__(self):
        return self.neighborhood_name

    neighborhood_name = models.CharField(max_length=200)


class AmbientTemp(models.Model):
    def __str__(self):
        return self.time
    neighborhood = models.ForeignKey("Neighborhood")
    time = models.IntegerField()
    temperature = models.FloatField()


class EnergyPrice(models.Model):
    neighborhood = models.ForeignKey("Neighborhood")
    time = models.IntegerField()
    price = models.FloatField()


class AvailableEnergy(models.Model):
    neighborhood = models.ForeignKey("Neighborhood")
    time = models.IntegerField()
    amount = models.FloatField()


class House(models.Model):
    def __str__(self):
        return self.house_name

    neighborhood = models.ForeignKey("Neighborhood")
    house_name = models.CharField(max_length=200)


class CalculatedConsumption(models.Model):
    house = models.ForeignKey("House")
    time = models.IntegerField()
    total_consumption = models.FloatField()


class FixedDemandProfile(models.Model):
    house = models.ForeignKey("House")
    time = models.IntegerField()
    consumption = models.FloatField()


class ThermoProfile(models.Model):
    house = models.ForeignKey("House")
    time = models.IntegerField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()


class Car(models.Model):
    house = models.ForeignKey("House")
    car_name = models.CharField(max_length=200)
    total_power_capacity = models.IntegerField()
    load_capacity = models.IntegerField()


class Room(models.Model):
    def __str__(self):
        return self.room_name + " in " + self.house.house_name

    house = models.ForeignKey("House")
    room_name = models.CharField(max_length=200)


### Appliance ###
class Appliance(models.Model):
    def __str__(self):
        return self.appliance_name

    room = models.ForeignKey("Room")
    appliance_name = models.CharField(max_length=200)

    # with 'abstract = True', there is no database entry for Appliance, but there will be database entries for classes
    #   that inherit from this class (such as FixedDemand)
    class Meta:
        abstract = True


class ShiftingLoadCycle(Appliance):
    because_there_has_to_be_something = models.FloatField(default=0)


class ShiftingLoadProfile(models.Model):
    shiftingloadcycle = models.ForeignKey("ShiftingLoadCycle")
    time = models.IntegerField()
    consumption = models.FloatField()


class HeatLoadVariablePower(Appliance):
    power_required = models.FloatField()                # PHEAT_HOUSE
    isolation_coefficient = models.FloatField()         # UA_HOUSE
    coefficient_of_performance = models.FloatField()    # COP_HOUSE
    mass_of_air = models.FloatField()                   # MASS_HOUSE


class HeatLoadInvariablePower(Appliance):
    power_required = models.FloatField()                # PCOOL_(REF/FREZ)
    isolation_coefficient = models.FloatField()         # UA_(REF/FREZ)
    coefficient_of_performance = models.FloatField()    # COP_(REF/FREZ)
    mass_of_air = models.FloatField()                   # MASS_(REF/FREZ)
    temperature_min_inside = models.FloatField()            # temp_house
    temperature_max_inside = models.FloatField()


class OnOffProfile(models.Model):
    shiftingloadcycle = models.ForeignKey("ShiftingLoadCycle", blank=True, null=True)
    heatloadinvariablepower = models.ForeignKey("HeatLoadInvariablePower", blank=True, null=True)
    heatloadvariablepower = models.ForeignKey("HeatLoadVariablePower", blank=True, null=True)
    car = models.ForeignKey("Car", blank=True, null=True)


class OnOffInfo(models.Model):
    onoffprofile = models.ForeignKey("OnOffProfile")
    time = models.IntegerField()
    on_off = models.IntegerField(default=0)
    info = models.IntegerField(default=0)

    @property
    def house(self):
        if self.onoffprofile.heatloadvariablepower is not None:
            return self.onoffprofile.heatloadvariablepower.room.house
        elif self.onoffprofile.shiftingloadcycle is not None:
            return self.onoffprofile.shiftingloadcycle.room.house
        elif self.onoffprofile.heatloadinvariablepower is not None:
            return self.onoffprofile.heatloadinvariablepower.room.house

    def appliance_name(self):
        if self.onoffprofile.heatloadvariablepower is not None:
            return self.onoffprofile.heatloadvariablepower.appliance_name
        elif self.onoffprofile.shiftingloadcycle is not None:
            return self.onoffprofile.shiftingloadcycle.appliance_name
        elif self.onoffprofile.heatloadinvariablepower is not None:
            return self.onoffprofile.heatloadinvariablepower.appliance_name


class Sensor(models.Model):
    def __str__(self):
        return self.sensor_name

    sensor_name = models.CharField(max_length=200)
    house = models.ForeignKey("House")
    value = models.FloatField()

"""
class Recording(models.Model):
    sensor = models.ForeignKey("Sensor")
    value = models.FloatField()
    timestamp = models.DateTimeField()
"""