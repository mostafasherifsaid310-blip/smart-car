from django.contrib import admin
from .models import MaintenanceRecord,MaintenancePart

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("car","technician","service_type","service_date","mileage",
        "cost","status",)

    list_filter = ("status","service_date",)

    search_fields = ("car__brand","car__model","car__license_plate",
        "technician__name","service_type",)

    ordering = ("-service_date",)
    
@admin.register(MaintenancePart)
class MaintenancePartAdmin(admin.ModelAdmin):

    list_display = ("maintenance","spare_part","quantity_used",)
    search_fields = ("spare_part__name","spare_part__part_number",)    