from django.db import models
from cars.models import Car
from technicians.models import Technician


class MaintenanceRecord(models.Model):
    STATUS_CHOICES=[
        ("completed", "Completed"),
        ("in_progress", "In Progress"),
        ("cancelled", "Cancelled"),]

    car=models.ForeignKey(Car,on_delete=models.CASCADE,related_name="maintenance_records")
    technician=models.ForeignKey(Technician,on_delete=models.PROTECT,related_name="maintenance_records")
    service_type=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    service_date=models.DateField()
    mileage=models.PositiveIntegerField()
    cost=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default="completed")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} - {self.service_type}"

class MaintenancePart(models.Model):
    maintenance=models.ForeignKey(MaintenanceRecord,on_delete=models.CASCADE,related_name="parts_used")
    spare_part=models.ForeignKey("spare_parts.SparePart",on_delete=models.PROTECT,related_name="maintenance_usages")
    quantity_used = models.PositiveIntegerField()

    class Meta:
        constraints=[models.UniqueConstraint(
                fields=["maintenance", "spare_part"],
                name="unique_maintenance_spare_part")]

    def __str__(self):
        return f"{self.spare_part} x {self.quantity_used}"
