from django.db import models
from cars.models import Car
from technicians.models import Technician


class Appointment(models.Model):

    STATUS_CHOICES=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),]

    car=models.ForeignKey(Car,on_delete=models.CASCADE,related_name="appointments")
    technician=models.ForeignKey(Technician,on_delete=models.PROTECT,related_name="appointments")
    service_type=models.CharField(max_length=100)
    appointment_date=models.DateField()
    appointment_time=models.TimeField()
    status=models.CharField(max_length=30,choices=STATUS_CHOICES,default="pending")
    notes=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} - {self.appointment_date}"
