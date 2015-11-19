from django.contrib import admin
from .models import *


# Neighborhood
class HouseInline(admin.StackedInline):
    model = House
    extra = 0


class PriceInline(admin.StackedInline):
    model = EnergyPrice
    extra = 94


class NeighborhoodAdmin(admin.ModelAdmin):
    inlines = [HouseInline, PriceInline]


# House
class RoomInline(admin.StackedInline):
    model = Room
    extra = 0


class HouseAdmin(admin.ModelAdmin):
    inlines = [RoomInline]


# Room


class ShiftingLoadCycleInline(admin.StackedInline):
    model = ShiftingLoadCycle
    extra = 0


class HeatloadVariablePowerInline(admin.StackedInline):
    model = HeatLoadVariablePower
    extra = 0


class HeatloadInvariablePowerInline(admin.StackedInline):
    model = HeatLoadInvariablePower
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    inlines = [ShiftingLoadCycleInline, HeatloadVariablePowerInline, HeatloadInvariablePowerInline]



# Appliance


admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(ShiftingLoadCycle)
admin.site.register(HeatLoadVariablePower)
admin.site.register(HeatLoadInvariablePower)
admin.site.register(Room, RoomAdmin)
admin.site.register(ShiftingLoadProfile)
admin.site.register(OnOffProfile)
admin.site.register(OnOffInfo)