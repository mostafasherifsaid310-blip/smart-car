from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cars")
    brand=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    year=models.PositiveIntegerField()
    license_plate=models.CharField(max_length=20,unique=True)
    mileage=models.PositiveIntegerField(default=0)
    color=models.CharField(max_length=50,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(mileage__gte=0),
                name="car_mileage_gte_0",),
            models.CheckConstraint(condition=models.Q(year__gte=1900) & models.Q(year__lte=2100),
                name="car_year_valid",),]

        indexes = [models.Index(fields=["owner"]),models.Index(fields=["brand", "model"]),]
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate}"
    
