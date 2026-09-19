from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cars.models import Car
from maintenance.models import MaintenanceRecord
from appointments.models import Appointment
from technicians.models import Technician
from spare_parts.models import SparePart


class Command(BaseCommand):
    help = "Setup default RBAC permissions"

    def handle(self, *args, **kwargs):

        models_permissions = {
            "Customer": {
                Car: ["view"],
                Appointment: ["view", "add"],
                MaintenanceRecord: ["view"],
                Technician: ["view"],
                SparePart: ["view"],
            },

            "Manager": {
                Car: ["view", "add", "change", "delete"],
                MaintenanceRecord: [
                    "view",
                    "add",
                    "change",
                    "delete",
                ],
                Appointment: [
                    "view",
                    "add",
                    "change",
                    "delete",
                ],
                Technician: [
                    "view",
                    "add",
                    "change",
                    "delete",
                ],
                SparePart: [
                    "view",
                    "add",
                    "change",
                    "delete",
                ],
            },
        }

        for role, model_permissions in models_permissions.items():

            group = Group.objects.get(name=role)

            for model, actions in model_permissions.items():

                content_type = ContentType.objects.get_for_model(model)

                for action in actions:

                    permission = Permission.objects.get(
                        content_type=content_type,
                        codename=f"{action}_{model._meta.model_name}",)

                    group.permissions.add(permission)

                    self.stdout.write(f"{role}: {permission.codename}")

        self.stdout.write(
            self.style.SUCCESS("RBAC permissions setup completed."))