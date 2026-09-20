from django import forms
from .models import Technician

class TechnicianForm(forms.ModelForm):

    class Meta:
        model = Technician

        fields = ["name","phone","email","specialization","experience_years","is_available",]

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Technician name"}),
            "phone": forms.TextInput(
                attrs={"placeholder": "Phone number"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email address"}),
            "specialization": forms.TextInput(
                attrs={"placeholder": "e.g. Engine, Electrical, Brakes"}),
            "experience_years": forms.NumberInput(
                attrs={"min": 0}),}