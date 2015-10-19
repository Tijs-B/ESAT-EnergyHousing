from django.contrib import admin
from .models import *


# Neighborhood
class HouseInline(admin.StackedInline):
    model = House
    extra = 0


class NeighborhoodAdmin(admin.ModelAdmin):
    fields = ['neighborhood_name', 'energy_price']
    inlines = [HouseInline]


# House
class RoomInline(admin.StackedInline):
    model = Room
    extra = 0


class HouseAdmin(admin.ModelAdmin):
    fields = ['house_name']
    inlines = [RoomInline]


# Room

class RoomsAdmin(admin.ModelAdmin):
    fields = ['room_name']


# Appliance
class ApplianceAdmin(admin.ModelAdmin):
    fields = ['appliance_name', 'priority']



admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(House, HouseAdmin)

admin.site.register(Room, RoomsAdmin)
