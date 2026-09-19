from django import forms
from .models import Car

class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = [
            "brand",
            "model",
            "year",
            "license_plate",
            "mileage",
            "color",]

        widgets = {"year": forms.NumberInput(
                attrs={"min": 1900,"max": 2100,}),
            "mileage": forms.NumberInput(attrs={"min": 0,}),}