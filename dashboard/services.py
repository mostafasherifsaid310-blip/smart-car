from django.db.models import F
from django.utils import timezone
from appointments.models import Appointment
from cars.models import Car
from maintenance.models import MaintenanceRecord
from spare_parts.models import SparePart
from technicians.models import Technician


def get_dashboard_data(user, is_manager_or_admin=False):

    if is_manager_or_admin:

        cars_count = Car.objects.count()

        maintenance_count = MaintenanceRecord.objects.count()

        appointments_count = Appointment.objects.count()

        technicians_count = Technician.objects.count()

        spare_parts_count = SparePart.objects.count()

        low_stock_parts = SparePart.objects.filter(quantity__lte=F("minimum_stock"))

        recent_maintenance = (MaintenanceRecord.objects
            .select_related("car", "technician")
            .order_by("-service_date", "-created_at")[:5])

        upcoming_appointments = (Appointment.objects
            .select_related("car", "technician")
            .filter(appointment_date__gte=user.date_joined.date())
            .order_by("appointment_date", "appointment_time")[:5])

    else:

        cars_count = Car.objects.filter(owner=user).count()

        maintenance_count = MaintenanceRecord.objects.filter(car__owner=user).count()

        appointments_count = Appointment.objects.filter(car__owner=user).count()

        technicians_count = Technician.objects.filter(is_available=True).count()

        spare_parts_count = SparePart.objects.count()

        low_stock_parts = SparePart.objects.filter(quantity__lte=F("minimum_stock"))

        recent_maintenance = (MaintenanceRecord.objects.filter(car__owner=user)
            .select_related("car", "technician")
            .order_by("-service_date", "-created_at")[:5])

        upcoming_appointments = (
            Appointment.objects.filter(
                car__owner=user,
                appointment_date__gte=timezone.localdate())
            .select_related("car", "technician")
            .order_by("appointment_date", "appointment_time")[:5])

    return {"cars_count": cars_count,
        "maintenance_count": maintenance_count,
        "appointments_count": appointments_count,
        "technicians_count": technicians_count,
        "spare_parts_count": spare_parts_count,
        "low_stock_parts": low_stock_parts,
        "recent_maintenance": recent_maintenance,
        "upcoming_appointments": upcoming_appointments,}