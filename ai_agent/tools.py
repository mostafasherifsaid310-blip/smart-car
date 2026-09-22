from django.core.exceptions import ValidationError
from cars.models import Car
from maintenance.models import MaintenanceRecord
from appointments.models import Appointment
from technicians.models import Technician
from django.utils import timezone
from datetime import date, time,datetime
from appointments.services import create_appointment
from maintenance.services import get_maintenance_history_for_car
from technicians.services import get_available_technicians_for_ai
from appointments.services import check_appointment_slot as service_check_appointment_slot
from appointments.services import (
    book_appointment_for_user,
    check_appointment_slot as service_check_appointment_slot,
)
from appointments.services import (
    book_appointment_for_user,
    check_appointment_slot_for_user,
)
from spare_parts.services import get_low_stock_parts


# def get_maintenance_history(user, car_id):
#     """
#     Return maintenance history for a car.

#     Security:
#     - User must be authenticated.
#     - Customer can only access their own car.
#     - Admin/Manager can access any car.
#     """

#     if not user or not user.is_authenticated:
#         raise ValidationError("Authentication required.")

#     try:
#         car = Car.objects.get(id=car_id)
#     except Car.DoesNotExist:
#         raise ValidationError("Car not found.")

#     is_staff_role = user.groups.filter(
#         name__in=["Admin", "Manager"]
#     ).exists()

#     if not is_staff_role and car.owner != user:
#         raise ValidationError(
#             "You do not have permission to access this car."
#         )

#     records = (
#         MaintenanceRecord.objects
#         .filter(car=car)
#         .select_related("technician")
#         .order_by("-service_date", "-created_at")
#     )

#     return {
#         "car_id": car.id,
#         "car": f"{car.brand} {car.model}",
#         "maintenance_count": records.count(),
#         "maintenance_history": [
#             {
#                 "id": record.id,
#                 "service_type": record.service_type,
#                 "service_date": str(record.service_date),
#                 "mileage": record.mileage,
#                 "cost": str(record.cost),
#                 "status": record.status,
#                 "technician": record.technician.name,
#             }
#             for record in records
#         ],
#     }
    
def get_maintenance_history(user, car_id):
    return get_maintenance_history_for_car(
        user=user,
        car_id=car_id,
    )    

# def find_available_technicians(user):
#     """
#     Return currently available technicians.

#     Security:
#     - User must be authenticated.
#     - Only available technicians are returned.
#     """

#     if not user or not user.is_authenticated:
#         raise ValidationError("Authentication required.")

#     technicians = (
#         Technician.objects
#         .filter(is_available=True)
#         .order_by("name")
#     )

#     return {
#         "technicians": [
#             {
#                 "id": technician.id,
#                 "name": technician.name,
#                 "specialization": technician.specialization,
#                 "experience_years": technician.experience_years,
#             }
#             for technician in technicians
#         ]
#     }    

def find_available_technicians(user):
    return get_available_technicians_for_ai(user)
    
# def check_appointment_slot(
#     user,
#     technician_id,
#     appointment_date,
#     appointment_time,
# ):
#     """
#     Check whether a technician is available at a specific date/time.
#     """

#     if not user or not user.is_authenticated:
#         raise ValidationError("Authentication required.")

#     try:
#         technician = Technician.objects.get(id=technician_id)
#     except Technician.DoesNotExist:
#         raise ValidationError("Technician not found.")

#     if not technician.is_available:
#         return {
#             "available": False,
#             "reason": "Technician is currently unavailable.",
#         }

#     appointment_exists = Appointment.objects.filter(
#         technician=technician,
#         appointment_date=appointment_date,
#         appointment_time=appointment_time,
#         status__in=[
#             "pending",
#             "confirmed",
#             "in_progress",
#         ],
#     ).exists()

#     if appointment_exists:
#         return {
#             "available": False,
#             "reason": "This appointment slot is already booked.",
#         }

#     return {
#         "available": True,
#         "technician": {
#             "id": technician.id,
#             "name": technician.name,
#             "specialization": technician.specialization,
#         },
#         "appointment_date": str(appointment_date),
#         "appointment_time": str(appointment_time),
#     }    

# def check_appointment_slot(
#     user,
#     technician_id,
#     appointment_date,
#     appointment_time,
# ):
#     if not user or not user.is_authenticated:
#         raise ValidationError("Authentication required.")

#     try:
#         technician = Technician.objects.get(id=technician_id)
#     except Technician.DoesNotExist:
#         raise ValidationError("Technician not found.")

#     if isinstance(appointment_date, str):
#         try:
#             appointment_date = date.fromisoformat(appointment_date)
#         except ValueError:
#             raise ValidationError("Invalid appointment date format.")

#     if isinstance(appointment_time, str):
#         try:
#             appointment_time = datetime.strptime(
#                 appointment_time,
#                 "%H:%M",
#             ).time()
#         except ValueError:
#             raise ValidationError("Invalid appointment time format.")

#     return service_check_appointment_slot(
#         technician=technician,
#         appointment_date=appointment_date,
#         appointment_time=appointment_time,
#     )

def check_appointment_slot(
    user,
    technician_id,
    appointment_date,
    appointment_time,
):
    if isinstance(appointment_date, str):
        try:
            appointment_date = date.fromisoformat(appointment_date)
        except ValueError:
            raise ValidationError("Invalid appointment date format.")

    if isinstance(appointment_time, str):
        try:
            appointment_time = datetime.strptime(
                appointment_time,
                "%H:%M",
            ).time()
        except ValueError:
            raise ValidationError("Invalid appointment time format.")

    return check_appointment_slot_for_user(
        user=user,
        technician_id=technician_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
    )
    
# def book_appointment(
#     user,
#     car_id,
#     technician_id,
#     service_type,
#     appointment_date,
#     appointment_time,
#     notes="",
# ):
#     """
#     AI Tool:
#     Creates an appointment through the business service layer.

#     The tool does NOT access the database directly for creation.
#     Permission and business validation are handled by the service.
#     """

#     if not user or not user.is_authenticated:
#         raise ValidationError("Authentication required.")

#     try:
#         car = Car.objects.get(id=car_id)
#     except Car.DoesNotExist:
#         raise ValidationError("Car not found.")

#     try:
#         technician = Technician.objects.get(id=technician_id)
#     except Technician.DoesNotExist:
#         raise ValidationError("Technician not found.")

#     if not service_type or not service_type.strip():
#         raise ValidationError("Service type is required.")

#     if isinstance(appointment_date, str):
#         try:
#             appointment_date = date.fromisoformat(appointment_date)
#         except ValueError:
#             raise ValidationError("Invalid appointment date format.")

#     if isinstance(appointment_time, str):
#         try:
#             appointment_time = datetime.strptime(
#                 appointment_time,
#                 "%H:%M"
#             ).time()
#         except ValueError:
#             raise ValidationError("Invalid appointment time format.")
    
#     if not isinstance(appointment_date, date):
#         raise ValidationError("Invalid appointment date.")

#     if not isinstance(appointment_time, time):
#         raise ValidationError("Invalid appointment time.")

#     appointment = create_appointment(
#         user=user,
#         car=car,
#         technician=technician,
#         service_type=service_type.strip(),
#         appointment_date=appointment_date,
#         appointment_time=appointment_time,
#         status="pending",
#         notes=notes.strip() if notes else "",
#     )

#     return {
#         "success": True,
#         "message": "Appointment booked successfully.",
#         "appointment": {
#             "id": appointment.id,
#             "car_id": appointment.car.id,
#             "car": f"{appointment.car.brand} {appointment.car.model}",
#             "technician_id": appointment.technician.id,
#             "technician": appointment.technician.name,
#             "service_type": appointment.service_type,
#             "appointment_date": str(appointment.appointment_date),
#             "appointment_time": str(appointment.appointment_time),
#             "status": appointment.status,
#             "notes": appointment.notes,
#         },
#     }

# def book_appointment(
#     user,
#     car_id,
#     technician_id,
#     service_type,
#     appointment_date,
#     appointment_time,
#     notes="",
# ):
#     if not user or not user.is_authenticated:
#         raise ValidationError("Authentication required.")

#     try:
#         car = Car.objects.get(id=car_id)
#     except Car.DoesNotExist:
#         raise ValidationError("Car not found.")

#     try:
#         technician = Technician.objects.get(id=technician_id)
#     except Technician.DoesNotExist:
#         raise ValidationError("Technician not found.")

#     if not service_type or not service_type.strip():
#         raise ValidationError("Service type is required.")

#     if isinstance(appointment_date, str):
#         try:
#             appointment_date = date.fromisoformat(appointment_date)
#         except ValueError:
#             raise ValidationError("Invalid appointment date format.")

#     if isinstance(appointment_time, str):
#         try:
#             appointment_time = datetime.strptime(
#                 appointment_time,
#                 "%H:%M",
#             ).time()
#         except ValueError:
#             raise ValidationError("Invalid appointment time format.")

#     if not isinstance(appointment_date, date):
#         raise ValidationError("Invalid appointment date.")

#     if not isinstance(appointment_time, time):
#         raise ValidationError("Invalid appointment time.")

#     appointment = create_appointment(
#         user=user,
#         car=car,
#         technician=technician,
#         service_type=service_type.strip(),
#         appointment_date=appointment_date,
#         appointment_time=appointment_time,
#         status="pending",
#         notes=notes.strip() if notes else "",
#     )

#     return {
#         "success": True,
#         "message": "Appointment booked successfully.",
#         "appointment": {
#             "id": appointment.id,
#             "car_id": appointment.car.id,
#             "car": f"{appointment.car.brand} {appointment.car.model}",
#             "technician_id": appointment.technician.id,
#             "technician": appointment.technician.name,
#             "service_type": appointment.service_type,
#             "appointment_date": str(appointment.appointment_date),
#             "appointment_time": str(appointment.appointment_time),
#             "status": appointment.status,
#             "notes": appointment.notes,
#         },
#     }

def book_appointment(
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

    if isinstance(appointment_date, str):
        try:
            appointment_date = date.fromisoformat(appointment_date)
        except ValueError:
            raise ValidationError("Invalid appointment date format.")

    if isinstance(appointment_time, str):
        try:
            appointment_time = datetime.strptime(
                appointment_time,
                "%H:%M",
            ).time()
        except ValueError:
            raise ValidationError("Invalid appointment time format.")

    appointment = book_appointment_for_user(
        user=user,
        car_id=car_id,
        technician_id=technician_id,
        service_type=service_type,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        notes=notes,
    )

    return {
        "success": True,
        "message": "Appointment booked successfully.",
        "appointment": {
            "id": appointment.id,
            "car_id": appointment.car.id,
            "car": f"{appointment.car.brand} {appointment.car.model}",
            "technician_id": appointment.technician.id,
            "technician": appointment.technician.name,
            "service_type": appointment.service_type,
            "appointment_date": str(appointment.appointment_date),
            "appointment_time": str(appointment.appointment_time),
            "status": appointment.status,
            "notes": appointment.notes,
        },
    }
    
def find_low_stock_spare_parts(user):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required.")

    if not user.groups.filter(name__in=["Admin", "Manager"]).exists():
        raise ValidationError(
            "You do not have permission to access spare parts inventory."
        )

    parts = get_low_stock_parts()

    return {
        "spare_parts": [
            {
                "id": part.id,
                "name": part.name,
                "part_number": part.part_number,
                "quantity": part.quantity,
                "minimum_stock": part.minimum_stock,
                "price": str(part.price),
            }
            for part in parts
        ]
    }    
    