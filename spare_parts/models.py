from django.db import models


class SparePart(models.Model):

    name=models.CharField(max_length=150)
    part_number=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    quantity=models.PositiveIntegerField(default=0)
    minimum_stock=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.part_number})"
