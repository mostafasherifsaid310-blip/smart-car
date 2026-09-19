from django.db import models

class Technician(models.Model):
    name=models.CharField(max_length=150)
    phone=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    specialization=models.CharField(max_length=100)
    experience_years=models.PositiveIntegerField(default=0)
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
