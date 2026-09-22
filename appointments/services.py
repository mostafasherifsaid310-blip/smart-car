from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from authentication.utils import is_admin, is_manager
from .models import Appointment
from cars.models import Car
from technicians.models import Technician
from datetime import date, time


def get_user_appointments(user):
    """
    Return appointments accessible to the current user.
    Admins and Managers can see all appointments.
    Customers can see appointments for their own cars.
    """
    if is_admin(user) or is_manager(user):
        return (Appointment.objects.select_related("car", "technician").order_by("appointment_date", "appointment_time"))

    return (Appointment.objects.select_related("car", "technician").filter(car__owner=user)
        .order_by("appointment_date", "appointment_time"))


# def check_appointment_slot(technician, appointment_date, appointment_time):
#     """
#     Check whether a technician is available for a specific date/time.
#     """

#     if not technician.is_available:
#         raise ValidationError("This technician is currently unavailable.")

#     exists = Appointment.objects.filter(
#         technician=technician,
#         appointment_date=appointment_date,
#         appointment_time=appointment_time,).exists()

#     if exists:
#         raise ValidationError(
#             "This technician already has an appointment at this time.")

#     return True

def check_appointment_slot(
    technician,
    appointment_date,
    appointment_time,
):
    if not isinstance(technician, Technician):
        raise ValidationError("Invalid technician.")

    if not technician.is_available:
        return {
            "available": False,
            "reason": "Technician is currently unavailable.",
        }

    appointment_exists = Appointment.objects.filter(
        technician=technician,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status__in=[
            "pending",
            "confirmed",
            "in_progress",
        ],
    ).exists()

    if appointment_exists:
        return {
            "available": False,
            "reason": "This appointment slot is already booked.",
        }

    return {
        "available": True,
        "technician": {
            "id": technician.id,
            "name": technician.name,
            "specialization": technician.specialization,
        },
        "appointment_date": str(appointment_date),
        "appointment_time": str(appointment_time),
    }

@transaction.atomic
def create_appointment(
    user,
    car,
    technician,
    service_type,
    appointment_date,
    appointment_time,
    status="pending",
    notes="",):
    """
    Create an appointment after validating ownership,
    technician availability, and appointment slot.
    """

    if not user.is_authenticated:
        raise ValidationError("Authentication required.")

    if not is_admin(user) and not is_manager(user):
        if car.owner != user:
            raise ValidationError(
                "You do not have permission to book an appointment for this car.")

    if not isinstance(car, Car):
        raise ValidationError("Invalid car.")

    if not isinstance(technician, Technician):
        raise ValidationError("Invalid technician.")

    check_appointment_slot(
        technician=technician,
        appointment_date=appointment_date,
        appointment_time=appointment_time,)

    try:
        appointment = Appointment.objects.create(
            car=car,
            technician=technician,
            service_type=service_type,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status=status,
            notes=notes,)
    except IntegrityError:
        raise ValidationError(
            "This appointment slot is already booked.")

    return appointment


@transaction.atomic
def cancel_appointment(user, appointment_id):
    """
    Cancel an appointment after checking user permission.
    """

    appointment = Appointment.objects.select_related(
        "car").get(id=appointment_id)

    if not is_admin(user) and not is_manager(user):
        if appointment.car.owner != user:
            raise ValidationError(
                "You do not have permission to cancel this appointment.")

    if appointment.status == "cancelled":
        raise ValidationError(
            "This appointment is already cancelled.")

    appointment.status = "cancelled"
    appointment.save(update_fields=["status"])

    return appointment

def book_appointment_for_user(
    user,
    car_id,
    technician_id,
    service_type,
    appointment_date,
    appointment_time,
    notes="",
):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required.")

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise ValidationError("Car not found.")

    try:
        technician = Technician.objects.get(id=technician_id)
    except Technician.DoesNotExist:
        raise ValidationError("Technician not found.")

    if not service_type or not service_type.strip():
        raise ValidationError("Service type is required.")

    if not isinstance(appointment_date, date):
        raise ValidationError("Invalid appointment date.")

    if not isinstance(appointment_time, time):
        raise ValidationError("Invalid appointment time.")

    return create_appointment(
        user=user,
        car=car,
        technician=technician,
        service_type=service_type.strip(),
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status="pending",
        notes=notes.strip() if notes else "",
    )
    
def check_appointment_slot_for_user(
    user,
    technician_id,
    appointment_date,
    appointment_time,
):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required.")

    try:
        technician = Technician.objects.get(id=technician_id)
    except Technician.DoesNotExist:
        raise ValidationError("Technician not found.")

    if not isinstance(appointment_date, date):
        raise ValidationError("Invalid appointment date.")

    if not isinstance(appointment_time, time):
        raise ValidationError("Invalid appointment time.")

    return check_appointment_slot(
        technician=technician,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
    )    