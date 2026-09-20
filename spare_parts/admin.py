from django.contrib import admin
from .models import SparePart


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):

    list_display = ("name","part_number","price","quantity","minimum_stock","created_at",)
    list_filter = ("created_at",)
    search_fields = ("name","part_number",)
    ordering = ("name",)