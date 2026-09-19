from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from authentication.utils import is_admin, is_manager
from .forms import CarForm
from .models import Car


@login_required
def car_list(request):
    if is_admin(request.user) or is_manager(request.user):
        cars = Car.objects.select_related("owner").all()
    else:
        cars = Car.objects.filter(owner=request.user)

    return render(request,"cars/car_list.html",{"cars": cars},)

@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if (
        car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        
        return HttpResponseForbidden("You do not have permission to access this car.")

    return render(request,"cars/car_detail.html",{"car": car},)

@login_required
def car_create(request):

    if request.method == "POST":
        form = CarForm(request.POST)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect("car_list")
    else:
        form = CarForm()

    return render(request,"cars/car_form.html",{"form": form,"title": "Add Car",},)

@login_required
def car_update(request, car_id):
    car = get_object_or_404(Car,id=car_id)

    if (
        car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to edit this car.")

    if request.method == "POST":

        form = CarForm(request.POST,instance=car)

        if form.is_valid():
            form.save()
            return redirect("car_detail",car_id=car.id)
    else:
        form = CarForm(instance=car)

    return render(request,"cars/car_form.html",{"form": form,"title": "Edit Car",},)

@login_required
def car_delete(request, car_id):

    car = get_object_or_404(Car,id=car_id)

    if (
        car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to delete this car.")

    if request.method == "POST":
        car.delete()
        return redirect("car_list")

    return render(request,"cars/car_confirm_delete.html",{"car": car},)