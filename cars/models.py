from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cars")
    brand=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    year=models.PositiveIntegerField()
    license_plate=models.CharField(max_length=20,unique=True)
    mileage=models.PositiveIntegerField(default=0)
    color=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate}"
    
