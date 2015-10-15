from django.contrib import admin
from .models import *




class HouseInline(admin.StackedInline):
    model = House
    extra = 3

class NeighborhoodAdmin(admin.ModelAdmin):
    fields = ['neighborhood_name', 'energy_price']
    inlines = [HouseInline]

admin.site.register(Neighborhood, NeighborhoodAdmin)

