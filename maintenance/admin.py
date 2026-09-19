from django.contrib import admin
from .models import MaintenanceRecord, MaintenancePart

admin.site.register(MaintenanceRecord)
admin.site.register(MaintenancePart)