from django.db.models import F
from django.utils import timezone
from appointments.models import Appointment
from cars.models import Car
from maintenance.models import MaintenanceRecord
from spare_parts.models import SparePart
from technicians.models import Technician


# def get_dashboard_data(user, is_manager_or_admin=False):

#     if is_manager_or_admin:

#         cars_count = Car.objects.count()

#         maintenance_count = MaintenanceRecord.objects.count()

#         appointments_count = Appointment.objects.count()

#         technicians_count = Technician.objects.count()

#         spare_parts_count = SparePart.objects.count()

#         low_stock_parts = SparePart.objects.filter(quantity__lte=F("minimum_stock"))

#         recent_maintenance = (MaintenanceRecord.objects
#             .select_related("car", "technician")
#             .order_by("-service_date", "-created_at")[:5])

#         upcoming_appointments = (Appointment.objects
#             .select_related("car", "technician")
#             .filter(appointment_date__gte=user.date_joined.date())
#             .order_by("appointment_date", "appointment_time")[:5])

#     else:

#         cars_count = Car.objects.filter(owner=user).count()

#         maintenance_count = MaintenanceRecord.objects.filter(car__owner=user).count()

#         appointments_count = Appointment.objects.filter(car__owner=user).count()

#         technicians_count = Technician.objects.filter(is_available=True).count()

#         spare_parts_count = SparePart.objects.count()

#         low_stock_parts = SparePart.objects.none()

#         recent_maintenance = (MaintenanceRecord.objects.filter(car__owner=user)
#             .select_related("car", "technician")
#             .order_by("-service_date", "-created_at")[:5])

#         upcoming_appointments = (
#             Appointment.objects.filter(
#                 car__owner=user,
#                 appointment_date__gte=timezone.localdate())
#             .select_related("car", "technician")
#             .order_by("appointment_date", "appointment_time")[:5])

#     return {"cars_count": cars_count,
#         "maintenance_count": maintenance_count,
#         "appointments_count": appointments_count,
#         "technicians_count": technicians_count,
#         "spare_parts_count": spare_parts_count,
#         "low_stock_parts": low_stock_parts,
#         "recent_maintenance": recent_maintenance,
#         "upcoming_appointments": upcoming_appointments,}

def get_dashboard_data(user, is_manager_or_admin=False):

    if is_manager_or_admin:

        # ============================================================
        # MANAGER / ADMIN
        # See ALL customers' cars, maintenance and appointments
        # ============================================================

        cars = (
            Car.objects
            .select_related("owner")
            .order_by("-id")
        )

        maintenance_records = (
            MaintenanceRecord.objects
            .select_related(
                "car",
                "car__owner",
                "technician",
            )
            .order_by(
                "-service_date",
                "-created_at",
            )
        )

        appointments = (
            Appointment.objects
            .select_related(
                "car",
                "car__owner",
                "technician",
            )
            .order_by(
                "appointment_date",
                "appointment_time",
            )
        )

        # Counts for ALL customers
        cars_count = cars.count()

        maintenance_count = maintenance_records.count()

        appointments_count = appointments.count()

        technicians_count = Technician.objects.count()

        spare_parts_count = SparePart.objects.count()

        # Manager/Admin can see low-stock parts
        low_stock_parts = SparePart.objects.filter(
            quantity__lte=F("minimum_stock")
        )

        # Dashboard shows latest 5 maintenance records
        recent_maintenance = maintenance_records[:5]

        # Dashboard shows upcoming appointments
        upcoming_appointments = appointments.filter(
            appointment_date__gte=timezone.localdate()
        )[:5]

    else:

        # ============================================================
        # CUSTOMER
        # See ONLY his own data
        # ============================================================

        cars = (
            Car.objects
            .filter(owner=user)
            .select_related("owner")
            .order_by("-id")
        )

        maintenance_records = (
            MaintenanceRecord.objects
            .filter(car__owner=user)
            .select_related(
                "car",
                "technician",
            )
            .order_by(
                "-service_date",
                "-created_at",
            )
        )

        appointments = (
            Appointment.objects
            .filter(car__owner=user)
            .select_related(
                "car",
                "technician",
            )
            .order_by(
                "appointment_date",
                "appointment_time",
            )
        )

        # Counts for THIS customer only
        cars_count = cars.count()

        maintenance_count = maintenance_records.count()

        appointments_count = appointments.count()

        technicians_count = Technician.objects.filter(
            is_available=True
        ).count()

        spare_parts_count = SparePart.objects.count()

        # Customer cannot see low-stock parts
        low_stock_parts = SparePart.objects.none()

        # Dashboard shows this customer's latest 5 records
        recent_maintenance = maintenance_records[:5]

        # Dashboard shows this customer's upcoming appointments
        upcoming_appointments = appointments.filter(
            appointment_date__gte=timezone.localdate()
        )[:5]

    return {
        "cars_count": cars_count,
        "maintenance_count": maintenance_count,
        "appointments_count": appointments_count,
        "technicians_count": technicians_count,
        "spare_parts_count": spare_parts_count,

        # Full QuerySets
        "cars": cars,
        "maintenance_records": maintenance_records,
        "appointments": appointments,

        # Dashboard sections
        "low_stock_parts": low_stock_parts,
        "recent_maintenance": recent_maintenance,
        "upcoming_appointments": upcoming_appointments,
    }