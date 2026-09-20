from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from authentication.utils import is_admin, is_manager
from cars.models import Car
from .forms import MaintenanceForm,MaintenancePartForm
from .models import MaintenanceRecord, MaintenancePart
from django.core.exceptions import ValidationError

@login_required
def maintenance_list(request):

    if is_admin(request.user) or is_manager(request.user):
        records = MaintenanceRecord.objects.select_related("car","technician").all()
    else:
        records = MaintenanceRecord.objects.select_related("car","technician").filter(
            car__owner=request.user)

    return render(request,"maintenance/maintenance_list.html",{"records": records})


@login_required
def maintenance_detail(request, maintenance_id):

    record = get_object_or_404(MaintenanceRecord,id=maintenance_id)

    if (
        record.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to view this maintenance record.")

    return render(request,"maintenance/maintenance_detail.html",{"record": record})

@login_required
def maintenance_create(request):

    if request.method == "POST":

        form = MaintenanceForm(request.POST)

        if form.is_valid():

            record = form.save(commit=False)

            if (
                not is_admin(request.user)
                and not is_manager(request.user)
                and record.car.owner != request.user):
                return HttpResponseForbidden(
                    "You can only add maintenance for your own cars.")

            record.save()

            return redirect("maintenance_list")
    else:
        form = MaintenanceForm()

    if not is_admin(request.user) and not is_manager(request.user):

        form.fields["car"].queryset = Car.objects.filter(owner=request.user)

    return render(
        request,"maintenance/maintenance_form.html",
        {
            "form": form,
            "title": "Add Maintenance Record"})

@login_required
def maintenance_update(request, maintenance_id):

    record = get_object_or_404(
        MaintenanceRecord,
        id=maintenance_id
    )

    if (
        record.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden(
            "You do not have permission to edit this maintenance record.")

    if request.method == "POST":

        form = MaintenanceForm(request.POST,instance=record)

        if form.is_valid():

            updated_record = form.save(commit=False)

            if (
                not is_admin(request.user)
                and not is_manager(request.user)
                and updated_record.car.owner != request.user):
                return HttpResponseForbidden(
                    "You can only use your own cars.")

            updated_record.save()

            return redirect("maintenance_detail",maintenance_id=record.id)
    else:

        form = MaintenanceForm(instance=record)

    if not is_admin(request.user) and not is_manager(request.user):

        form.fields["car"].queryset = Car.objects.filter(
            owner=request.user)

    return render(
        request,
        "maintenance/maintenance_form.html",
        {
            "form": form,
            "title": "Edit Maintenance Record"
        })


@login_required
def maintenance_delete(request, maintenance_id):

    record = get_object_or_404(
        MaintenanceRecord,
        id=maintenance_id)

    if (
        record.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden(
            "You do not have permission to delete this maintenance record.")

    if request.method == "POST":

        record.delete()

        return redirect("maintenance_list")

    return render(request,"maintenance/maintenance_confirm_delete.html",
        {"record": record})
    

@login_required
def maintenance_add_part(request, maintenance_id):

    record = get_object_or_404(MaintenanceRecord,id=maintenance_id)

    if (
        record.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden(
        "You do not have permission to modify this maintenance record.")

    if request.method == "POST":

        form = MaintenancePartForm(request.POST)

        if form.is_valid():

            spare_part = form.cleaned_data["spare_part"]

            quantity_used = form.cleaned_data[
                "quantity_used"]

            try:

                from .services import use_spare_part

                use_spare_part(maintenance_record=record,spare_part=spare_part,
                    quantity_used=quantity_used)

                return redirect("maintenance_detail",maintenance_id=record.id)

            except ValidationError as error:

                form.add_error("quantity_used",error.message)

    else:

        form = MaintenancePartForm()

    return render(request,"maintenance/maintenance_add_part.html",{"form": form,"record": record})    

@login_required
def maintenance_remove_part(
    request,
    maintenance_part_id):

    if request.method != "POST":
        return HttpResponseForbidden("POST request required.")

    maintenance_part = get_object_or_404(MaintenancePart,id=maintenance_part_id)

    record = maintenance_part.maintenance

    if (
        record.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden(
            "You do not have permission to modify this maintenance record.")

    from .services import remove_spare_part

    remove_spare_part(maintenance_part_id)

    return redirect("maintenance_detail",maintenance_id=record.id)