# from django.db import transaction
# from django.core.exceptions import ValidationError
# from .models import MaintenanceRecord, MaintenancePart
# from spare_parts.models import SparePart


# @transaction.atomic
# def use_spare_part(
#     maintenance_record,
#     spare_part,
#     quantity_used):
#     """
#     Add a spare part to a maintenance record
#     and decrease its stock safely.
#     """

#     if quantity_used <= 0:
#         raise ValidationError(
#             "Quantity used must be greater than zero.")

#     spare_part = (SparePart.objects.select_for_update().get(id=spare_part.id))

#     if spare_part.quantity < quantity_used:
#         raise ValidationError(
#             f"Insufficient stock. "
#             f"Available: {spare_part.quantity}")

#     maintenance_part, created = (
#         MaintenancePart.objects.get_or_create(
#             maintenance=maintenance_record,
#             spare_part=spare_part,
#             defaults={"quantity_used": quantity_used}))

#     if not created:

#         maintenance_part.quantity_used += quantity_used
#         maintenance_part.save(update_fields=["quantity_used"])

#     spare_part.quantity -= quantity_used

#     spare_part.save(update_fields=["quantity"])

#     return maintenance_part

# @transaction.atomic
# def remove_spare_part(
#     maintenance_part_id):
#     """
#     Remove a spare part usage from a maintenance record
#     and return the quantity back to stock.
#     """

#     maintenance_part = (
#         MaintenancePart.objects
#         .select_related("spare_part")
#         .select_for_update()
#         .get(id=maintenance_part_id))

#     spare_part = (SparePart.objects
#         .select_for_update()
#         .get(id=maintenance_part.spare_part.id))

#     quantity = maintenance_part.quantity_used

#     spare_part.quantity += quantity

#     spare_part.save(update_fields=["quantity"])

#     maintenance_part.delete()


from django.core.exceptions import ValidationError
from django.db import transaction
from .models import MaintenanceRecord, MaintenancePart
from cars.models import Car
from technicians.models import Technician
from spare_parts.models import SparePart


def get_user_maintenance_records(user):
    """
    Return maintenance records accessible to the current user.
    Customers see records for their own cars.
    Staff can see all records.
    """
    if user.groups.filter(name__in=["Admin", "Manager"]).exists():
        return (
            MaintenanceRecord.objects
            .select_related("car", "technician")
            .prefetch_related("parts_used__spare_part")
            .order_by("-service_date", "-created_at"))

    return (
        MaintenanceRecord.objects
        .filter(car__owner=user)
        .select_related("car", "technician")
        .prefetch_related("parts_used__spare_part")
        .order_by("-service_date", "-created_at"))


def get_maintenance_record(maintenance_id):
    """
    Return a maintenance record by ID.
    """
    try:
        return (
            MaintenanceRecord.objects
            .select_related("car", "technician")
            .prefetch_related("parts_used__spare_part")
            .get(id=maintenance_id))
    except MaintenanceRecord.DoesNotExist:
        raise ValidationError("Maintenance record not found.")


def create_maintenance(
    user,
    car,
    technician,
    service_type,
    service_date,
    mileage,
    cost=0,
    description="",
    status="completed",):
    """
    Create a maintenance record after validating
    ownership and basic business rules.
    """

    if not user.is_authenticated:
        raise ValidationError("Authentication required.")

    if not isinstance(car, Car):
        raise ValidationError("Invalid car.")

    if not isinstance(technician, Technician):
        raise ValidationError("Invalid technician.")

    is_staff_role = user.groups.filter(
        name__in=["Admin", "Manager"]).exists()

    if not is_staff_role and car.owner != user:
        raise ValidationError(
            "You do not have permission to create maintenance "
            "for this car.")

    if mileage < 0:
        raise ValidationError(
            "Mileage cannot be negative.")

    if cost < 0:
        raise ValidationError(
            "Cost cannot be negative.")

    return MaintenanceRecord.objects.create(
        car=car,
        technician=technician,
        service_type=service_type,
        service_date=service_date,
        mileage=mileage,
        cost=cost,
        description=description,
        status=status,)


@transaction.atomic
def use_spare_part(
    maintenance_record,
    spare_part,
    quantity_used,):
    """
    Use a spare part in a maintenance record
    and decrease its stock atomically.
    """

    if quantity_used <= 0:
        raise ValidationError(
            "Quantity used must be greater than zero.")

    if not isinstance(maintenance_record, MaintenanceRecord):
        raise ValidationError(
            "Invalid maintenance record.")

    if not isinstance(spare_part, SparePart):
        raise ValidationError(
            "Invalid spare part.")

    spare_part = (
        SparePart.objects
        .select_for_update()
        .get(id=spare_part.id))

    if spare_part.quantity < quantity_used:
        raise ValidationError(
            f"Insufficient stock. "
            f"Available: {spare_part.quantity}")

    maintenance_part, created = (
        MaintenancePart.objects.get_or_create(
            maintenance=maintenance_record,
            spare_part=spare_part,
            defaults={
                "quantity_used": quantity_used},))

    if not created:
        maintenance_part.quantity_used += quantity_used
        maintenance_part.save(
            update_fields=["quantity_used"])

    spare_part.quantity -= quantity_used
    spare_part.save(
        update_fields=["quantity"])

    return maintenance_part


@transaction.atomic
def remove_spare_part(maintenance_part_id):
    """
    Remove a spare part from a maintenance record
    and return its quantity to stock.
    """

    try:
        maintenance_part = (
            MaintenancePart.objects
            .select_related("spare_part")
            .select_for_update()
            .get(id=maintenance_part_id))
    except MaintenancePart.DoesNotExist:
        raise ValidationError(
            "Maintenance part record not found.")

    spare_part = (
        SparePart.objects
        .select_for_update()
        .get(
            id=maintenance_part.spare_part.id))

    quantity = maintenance_part.quantity_used

    spare_part.quantity += quantity
    spare_part.save(
        update_fields=["quantity"])

    maintenance_part.delete()

    return spare_part

def get_maintenance_history_for_car(user, car_id):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required.")

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise ValidationError("Car not found.")

    is_staff_role = user.groups.filter(
        name__in=["Admin", "Manager"]
    ).exists()

    if not is_staff_role and car.owner != user:
        raise ValidationError(
            "You do not have permission to access this car."
        )

    records = (
        MaintenanceRecord.objects
        .filter(car=car)
        .select_related("technician")
        .order_by("-service_date", "-created_at")
    )

    return {
        "car_id": car.id,
        "car": f"{car.brand} {car.model}",
        "maintenance_count": records.count(),
        "maintenance_history": [
            {
                "id": record.id,
                "service_type": record.service_type,
                "service_date": str(record.service_date),
                "mileage": record.mileage,
                "cost": str(record.cost),
                "status": record.status,
                "technician": record.technician.name,
            }
            for record in records
        ],
    }