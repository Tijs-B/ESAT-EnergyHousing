from django.contrib import admin
from .models import *

# Register your models here.
class HouseInline(admin.StackedInline):
    model = House
    extra = 0

class NeighborhoodAdmin(admin.ModelAdmin):
    fields = ['neighborhood_name', 'energy_price']
    inlines = [HouseInline]

class VariablepowerAdmin(admin.ModelAdmin):
    fields = ['temprange','powerrange']

class RoomsAdmin(admin.ModelAdmin):
    fields = ['room_name']

class ApplianceAdmin(admin.ModelAdmin):
    fields = ['appliance_name']

admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(House)
admin.site.register(Variablepower, VariablepowerAdmin)
admin.site.register(Room)
admin.site.register(Appliance)
admin.site.register(Heatload)
