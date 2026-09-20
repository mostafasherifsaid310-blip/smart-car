from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = ["car","technician","service_type","appointment_date","appointment_time","status","notes",]

        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time"}),

            "notes": forms.Textarea(attrs={"rows": 4}),}