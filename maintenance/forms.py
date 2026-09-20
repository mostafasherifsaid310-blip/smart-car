from django import forms
from .models import MaintenanceRecord
from spare_parts.models import SparePart


class MaintenanceForm(forms.ModelForm):

    class Meta:
        model = MaintenanceRecord
        fields = ["car","technician","service_type","description","service_date","mileage","cost",
        "status",]

        widgets = {"service_date": forms.DateInput(attrs={"type": "date"}),
            "mileage": forms.NumberInput(attrs={"min": 0}),
            "cost": forms.NumberInput(attrs={"min": 0,"step": "0.01"}),
            "description": forms.Textarea(attrs={"rows": 4}),}

class MaintenancePartForm(forms.Form):

    spare_part = forms.ModelChoiceField(queryset=SparePart.objects.all(),label="Spare Part")
    quantity_used = forms.IntegerField(min_value=1,label="Quantity Used")        
        