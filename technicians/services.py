from django.core.exceptions import ValidationError
from .models import Technician


def get_all_technicians():
    """
    Return all technicians ordered by availability and name.
    """
    return (
        Technician.objects
        .all()
        .order_by("-is_available", "name")
    )


def get_available_technicians():
    """
    Return only technicians who are currently available.
    """
    return (
        Technician.objects
        .filter(is_available=True)
        .order_by("name")
    )


def get_technician(technician_id):
    """
    Return a technician by ID.
    """
    try:
        return Technician.objects.get(id=technician_id)
    except Technician.DoesNotExist:
        raise ValidationError("Technician not found.")


def create_technician(
    name,
    phone="",
    email="",
    specialization="",
    experience_years=0,
    is_available=True,
):
    """
    Create a technician after validating the data.
    """

    if experience_years < 0:
        raise ValidationError(
            "Experience years cannot be negative."
        )

    return Technician.objects.create(
        name=name,
        phone=phone,
        email=email,
        specialization=specialization,
        experience_years=experience_years,
        is_available=is_available,
    )


def set_technician_availability(technician_id, is_available):
    """
    Update technician availability.
    """

    technician = get_technician(technician_id)

    technician.is_available = is_available
    technician.save(update_fields=["is_available"])

    return technician


def get_available_technicians_by_specialization(
    specialization
):
    """
    Return available technicians matching a specialization.
    """

    if not specialization:
        raise ValidationError(
            "Specialization is required."
        )

    return (
        Technician.objects
        .filter(
            is_available=True,
            specialization__iexact=specialization,
        )
        .order_by("name")
    )
    
def get_available_technicians_for_ai(user):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required.")

    technicians = get_available_technicians()

    return {
        "technicians": [
            {
                "id": technician.id,
                "name": technician.name,
                "specialization": technician.specialization,
                "experience_years": technician.experience_years,
            }
            for technician in technicians
        ]
    }    