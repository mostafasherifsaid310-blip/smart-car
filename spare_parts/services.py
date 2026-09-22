from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from .models import SparePart


def get_all_spare_parts():
    """
    Return all spare parts ordered by name.
    """
    return SparePart.objects.all().order_by("name")


def get_low_stock_parts():
    """
    Return spare parts whose quantity is at or below
    the configured minimum stock.
    """
    return SparePart.objects.filter(
        quantity__lte=F("minimum_stock")
    ).order_by("name")


def get_spare_part(spare_part_id):
    """
    Return a spare part by ID.
    """
    try:
        return SparePart.objects.get(id=spare_part_id)
    except SparePart.DoesNotExist:
        raise ValidationError("Spare part not found.")


def create_spare_part(
    name,
    part_number,
    description="",
    price=0,
    quantity=0,
    minimum_stock=0,
):
    """
    Create a spare part after validating its values.
    """

    if price < 0:
        raise ValidationError("Price cannot be negative.")

    if quantity < 0:
        raise ValidationError("Quantity cannot be negative.")

    if minimum_stock < 0:
        raise ValidationError("Minimum stock cannot be negative.")

    return SparePart.objects.create(
        name=name,
        part_number=part_number,
        description=description,
        price=price,
        quantity=quantity,
        minimum_stock=minimum_stock,
    )


@transaction.atomic
def add_stock(spare_part_id, quantity):
    """
    Increase the stock of a spare part.
    """

    if quantity <= 0:
        raise ValidationError(
            "Quantity to add must be greater than zero."
        )

    spare_part = (
        SparePart.objects
        .select_for_update()
        .get(id=spare_part_id)
    )

    spare_part.quantity += quantity
    spare_part.save(update_fields=["quantity"])

    return spare_part


@transaction.atomic
def remove_stock(spare_part_id, quantity):
    """
    Decrease the stock of a spare part safely.
    """

    if quantity <= 0:
        raise ValidationError(
            "Quantity to remove must be greater than zero."
        )

    spare_part = (
        SparePart.objects
        .select_for_update()
        .get(id=spare_part_id)
    )

    if spare_part.quantity < quantity:
        raise ValidationError(
            f"Insufficient stock. Available: {spare_part.quantity}"
        )

    spare_part.quantity -= quantity
    spare_part.save(update_fields=["quantity"])

    return spare_part