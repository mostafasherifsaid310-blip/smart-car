from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.deletion import ProtectedError
from authentication.utils import is_admin, is_manager
from .forms import TechnicianForm
from .models import Technician


def management_access_required(user):
    return is_admin(user) or is_manager(user)


@login_required
def technician_list(request):

    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to manage technicians.")

    technicians = Technician.objects.all().order_by("-is_available","name",)

    return render(request,
        "technicians/technician_list.html",{"technicians": technicians,},)


@login_required
def technician_detail(request, technician_id):

    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to view technicians.")

    technician = get_object_or_404(Technician,id=technician_id,)

    return render(
        request,
        "technicians/technician_detail.html",{"technician": technician,},)


@login_required
def technician_create(request):

    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to create technicians.")

    if request.method == "POST":

        form = TechnicianForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("technician_list")

    else:
        form = TechnicianForm()

    return render(request,
        "technicians/technician_form.html",
        {"form": form,"title": "Add Technician",},)


@login_required
def technician_update(request, technician_id):

    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to edit technicians.")

    technician = get_object_or_404(Technician,id=technician_id,)

    if request.method == "POST":

        form = TechnicianForm(request.POST,instance=technician,)

        if form.is_valid():
            form.save()

            return redirect("technician_detail",technician_id=technician.id,)

    else:
        form = TechnicianForm(instance=technician,)

    return render(request,
        "technicians/technician_form.html",
        {"form": form,"title": "Edit Technician",},)


@login_required
def technician_delete(request, technician_id):

    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to delete technicians."
        )

    technician = get_object_or_404(
        Technician,
        id=technician_id,
    )

    if request.method == "POST":

        try:

            technician.delete()

            return redirect("technician_list")

        except ProtectedError:

            return render(
                request,
                "technicians/technician_confirm_delete.html",
                {
                    "technician": technician,
                    "delete_error": (
                        "This technician cannot be deleted because "
                        "they are linked to existing maintenance records "
                        "or appointments."
                    ),
                },
                status=400,
            )

    return render(
        request,
        "technicians/technician_confirm_delete.html",
        {
            "technician": technician,
        },
    )