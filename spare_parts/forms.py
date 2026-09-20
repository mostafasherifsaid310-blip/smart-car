from django import forms
from .models import SparePart

class SparePartForm(forms.ModelForm):

    class Meta:
        model = SparePart

        fields = ["name","part_number","description","price","quantity","minimum_stock",]
        widgets = {"description": forms.Textarea(attrs={"rows": 4}),

            "price": forms.NumberInput(attrs={"min": 0,"step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"min": 0}),
            "minimum_stock": forms.NumberInput(attrs={"min": 0}),}