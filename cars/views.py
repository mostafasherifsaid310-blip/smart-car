# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from django.shortcuts import get_object_or_404, redirect, render
# from authentication.utils import is_admin, is_manager
# from .forms import CarForm
# from .models import Car


# @login_required
# def car_list(request):
#     if is_admin(request.user) or is_manager(request.user):
#         cars = Car.objects.select_related("owner").all()
#     else:
#         cars = Car.objects.filter(owner=request.user)

#     return render(request,"cars/car_list.html",{"cars": cars},)

# @login_required
# def car_detail(request, car_id):
#     car = get_object_or_404(Car, id=car_id)

#     if (
#         car.owner != request.user
#         and not is_admin(request.user)
#         and not is_manager(request.user)):
        
#         return HttpResponseForbidden("You do not have permission to access this car.")

#     return render(request,"cars/car_detail.html",{"car": car},)

# @login_required
# def car_create(request):

#     if request.method == "POST":
#         form = CarForm(request.POST)

#         if form.is_valid():
#             car = form.save(commit=False)
#             car.owner = request.user
#             car.save()
#             return redirect("car_list")
#     else:
#         form = CarForm()

#     return render(request,"cars/car_form.html",{"form": form,"title": "Add Car",},)

# @login_required
# def car_update(request, car_id):
#     car = get_object_or_404(Car,id=car_id)

#     if (
#         car.owner != request.user
#         and not is_admin(request.user)
#         and not is_manager(request.user)):
#         return HttpResponseForbidden("You do not have permission to edit this car.")

#     if request.method == "POST":

#         form = CarForm(request.POST,instance=car)

#         if form.is_valid():
#             form.save()
#             return redirect("car_detail",car_id=car.id)
#     else:
#         form = CarForm(instance=car)

#     return render(request,"cars/car_form.html",{"form": form,"title": "Edit Car",},)

# @login_required
# def car_delete(request, car_id):

#     car = get_object_or_404(Car,id=car_id)

#     if (
#         car.owner != request.user
#         and not is_admin(request.user)
#         and not is_manager(request.user)):
#         return HttpResponseForbidden("You do not have permission to delete this car.")

#     if request.method == "POST":
#         car.delete()
#         return redirect("car_list")

#     return render(request,"cars/car_confirm_delete.html",{"car": car},)

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from authentication.utils import is_admin, is_manager
from .forms import CarForm
from .services import (
    get_user_cars,
    get_car_for_user,
    create_car,
    update_car,)


@login_required
def car_list(request):
    if is_admin(request.user) or is_manager(request.user):
        from .models import Car

        cars = Car.objects.select_related("owner").all()
    else:
        cars = get_user_cars(request.user)

    return render(
        request,
        "cars/car_list.html",
        {"cars": cars},
    )


@login_required
def car_detail(request, car_id):
    if is_admin(request.user) or is_manager(request.user):
        from .models import Car

        try:
            car = Car.objects.select_related("owner").get(
                id=car_id
            )
        except Car.DoesNotExist:
            return HttpResponseForbidden("Car not found.")
    else:
        try:
            car = get_car_for_user(
                request.user,
                car_id,
            )
        except ValidationError as error:
            return HttpResponseForbidden(error.message)

    return render(
        request,
        "cars/car_detail.html",
        {"car": car},
    )


@login_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST)

        if form.is_valid():
            data = {
                field: form.cleaned_data[field]
                for field in form.fields
            }

            try:
                create_car(
                    user=request.user,
                    **data,
                )

                return redirect("car_list")

            except ValidationError as error:
                form.add_error(None, error.message)

    else:
        form = CarForm()

    return render(
        request,
        "cars/car_form.html",
        {
            "form": form,
            "title": "Add Car",
        },
    )


@login_required
def car_update(request, car_id):
    if is_admin(request.user) or is_manager(request.user):
        from .models import Car

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return HttpResponseForbidden("Car not found.")
    else:
        try:
            car = get_car_for_user(
                request.user,
                car_id,
            )
        except ValidationError as error:
            return HttpResponseForbidden(error.message)

    if request.method == "POST":
        form = CarForm(
            request.POST,
            instance=car,
        )

        if form.is_valid():
            data = {
                field: form.cleaned_data[field]
                for field in form.fields
            }

            try:
                update_car(
                    user=request.user,
                    car_id=car_id,
                    **data,
                )

                return redirect(
                    "car_detail",
                    car_id=car.id,
                )

            except ValidationError as error:
                form.add_error(None, error.message)

    else:
        form = CarForm(instance=car)

    return render(
        request,
        "cars/car_form.html",
        {
            "form": form,
            "title": "Edit Car",
        },
    )


@login_required
def car_delete(request, car_id):
    from .models import Car

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return HttpResponseForbidden("Car not found.")

    if (
        car.owner != request.user
        and not is_admin(request.user)
        and not is_manager(request.user)
    ):
        return HttpResponseForbidden(
            "You do not have permission to delete this car."
        )

    if request.method == "POST":
        car.delete()
        return redirect("car_list")

    return render(
        request,
        "cars/car_confirm_delete.html",
        {"car": car},
    )