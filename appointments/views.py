from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from authentication.utils import is_admin, is_manager
from cars.models import Car
from .forms import AppointmentForm
from .models import Appointment


@login_required
def appointment_list(request):

    if is_admin(request.user) or is_manager(request.user):
        appointments = Appointment.objects.select_related("car","technician").all()

    else:
        appointments = Appointment.objects.select_related(
            "car","technician").filter(car__owner=request.user)

    return render(
        request,"appointments/appointment_list.html",{"appointments": appointments})


@login_required
def appointment_detail(request, appointment_id):

    appointment = get_object_or_404(Appointment,id=appointment_id)

    if (appointment.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden(
            "You do not have permission to view this appointment.")

    return render(
        request,"appointments/appointment_detail.html",{"appointment": appointment})


@login_required
def appointment_create(request):

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            if (
                not is_admin(request.user)
                and not is_manager(request.user)
                and appointment.car.owner != request.user):
                return HttpResponseForbidden(
                    "You can only create appointments for your own cars.")

            appointment.save()

            return redirect("appointment_list")

    else:
        form = AppointmentForm()

    if not is_admin(request.user) and not is_manager(request.user):

        form.fields["car"].queryset = Car.objects.filter(owner=request.user)

    return render(request,
        "appointments/appointment_form.html",
        {"form": form,"title": "Add Appointment"})


@login_required
def appointment_update(request, appointment_id):

    appointment = get_object_or_404(Appointment,
        id=appointment_id)

    if (appointment.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden(
            "You do not have permission to edit this appointment.")

    if request.method == "POST":

        form = AppointmentForm(
            request.POST,
            instance=appointment
        )

        if form.is_valid():

            updated_appointment = form.save(commit=False)

            if (not is_admin(request.user)
                and not is_manager(request.user)
                and updated_appointment.car.owner != request.user):
                return HttpResponseForbidden(
                    "You can only use your own cars.")

            updated_appointment.save()

            return redirect("appointment_detail",appointment_id=appointment.id)

    else:

        form = AppointmentForm(instance=appointment)

    if not is_admin(request.user) and not is_manager(request.user):

        form.fields["car"].queryset = Car.objects.filter(owner=request.user)

    return render(request,
        "appointments/appointment_form.html",
        {"form": form,"title": "Edit Appointment"})


@login_required
def appointment_delete(request, appointment_id):

    appointment = get_object_or_404(Appointment,id=appointment_id)

    if (appointment.car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden(
            "You do not have permission to delete this appointment.")

    if request.method == "POST":

        appointment.delete()

        return redirect("appointment_list")

    return render(request,
        "appointments/appointment_confirm_delete.html",
        {"appointment": appointment})