from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = ("car","technician","service_type","appointment_date","appointment_time","status",)
    list_filter = ("status","appointment_date",)
    search_fields = ("car__license_plate","car__brand","car__model","technician__name","service_type",)