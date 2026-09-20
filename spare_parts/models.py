from django.db import models


class SparePart(models.Model):

    name=models.CharField(max_length=150)
    part_number=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    quantity=models.PositiveIntegerField(default=0)
    minimum_stock=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="spare_part_price_gte_0",),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=0),
                name="spare_part_quantity_gte_0",),
            models.CheckConstraint(
                condition=models.Q(minimum_stock__gte=0),
                name="spare_part_minimum_stock_gte_0",),]

        indexes = [models.Index(fields=["name"]),
            models.Index(fields=["quantity"]),
            models.Index(fields=["minimum_stock"]),]


    def __str__(self):
        return f"{self.name} ({self.part_number})"
