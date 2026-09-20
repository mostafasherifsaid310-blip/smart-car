from django.db import transaction
from django.core.exceptions import ValidationError
from .models import MaintenanceRecord, MaintenancePart
from spare_parts.models import SparePart


@transaction.atomic
def use_spare_part(
    maintenance_record,
    spare_part,
    quantity_used):
    """
    Add a spare part to a maintenance record
    and decrease its stock safely.
    """

    if quantity_used <= 0:
        raise ValidationError(
            "Quantity used must be greater than zero.")

    spare_part = (SparePart.objects.select_for_update().get(id=spare_part.id))

    if spare_part.quantity < quantity_used:
        raise ValidationError(
            f"Insufficient stock. "
            f"Available: {spare_part.quantity}")

    maintenance_part, created = (
        MaintenancePart.objects.get_or_create(
            maintenance=maintenance_record,
            spare_part=spare_part,
            defaults={"quantity_used": quantity_used}))

    if not created:

        maintenance_part.quantity_used += quantity_used
        maintenance_part.save(update_fields=["quantity_used"])

    spare_part.quantity -= quantity_used

    spare_part.save(update_fields=["quantity"])

    return maintenance_part

@transaction.atomic
def remove_spare_part(
    maintenance_part_id):
    """
    Remove a spare part usage from a maintenance record
    and return the quantity back to stock.
    """

    maintenance_part = (
        MaintenancePart.objects
        .select_related("spare_part")
        .select_for_update()
        .get(id=maintenance_part_id))

    spare_part = (SparePart.objects
        .select_for_update()
        .get(id=maintenance_part.spare_part.id))

    quantity = maintenance_part.quantity_used

    spare_part.quantity += quantity

    spare_part.save(update_fields=["quantity"])

    maintenance_part.delete()