from django.db import models


class Neighborhood(models.Model):
    def __str__(self):
        return self.neighborhood_name
    neighborhood_name = models.CharField(max_length=200)
    energy_price = models.FloatField(default=1)
    ambient_temperature = models.FloatField()   # TEMP_AMB(t)
    power_consumed = models.FloatField()        # dfr_totaal


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
    time_of_cycle = models.TimeField()
    car_min_charge = models.FloatField(blank=True, null=True)
    car_current_charge = models.FloatField(blank=True, null=True)


class HeatLoadVariablePower(Appliance):
#    temperature_min = models.FloatField()
#    temperature_max = models.FloatField()
#    power_min = models.FloatField()
#    power_max = models.FloatField()
    power_required = models.FloatField()                # PHEAT_HOUSE
    isolation_coefficient = models.FloatField()         # UA_HOUSE
    coefficient_of_performance = models.FloatField()    # COP_HOUSE
    mass_of_air = models.FloatField()                   # MASS_HOUSE
    power_consumed = models.FloatField()                # dfr_house
#    temperature_inside = models.FloatField()            # temp_house


class HeatLoadInvariablePower(Appliance):
#    temperature_min = models.FloatField()
#    temperature_max = models.FloatField()
    power_required = models.FloatField()                # PCOOL_(REF/FREZ)
    isolation_coefficient = models.FloatField()         # UA_(REF/FREZ)
    coefficient_of_performance = models.FloatField()    # COP_(REF/FREZ)
    mass_of_air = models.FloatField()                   # MASS_(REF/FREZ)
    power_consumed = models.FloatField()                # dfr_(ref/frez)
#    temperature_inside = models.FloatField()            # temp_(ref/frez)


class ConsumptionProfile(models.Model):
    def __str__(self):
        return self.appliance.appliance_name + " " + str(self.order)
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
