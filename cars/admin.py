from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = ("id","owner","brand","model","license_plate","year","mileage",)
    search_fields = ("license_plate","brand","model","owner__username",)
    list_filter = ("brand","year",)