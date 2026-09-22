from django.core.exceptions import ValidationError
from .models import Car


def get_user_cars(user):
    return Car.objects.filter(owner=user).order_by("-created_at")


def get_car_for_user(user, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise ValidationError("Car not found.")

    if car.owner != user:
        raise ValidationError("You do not have permission to access this car.")

    return car


def create_car(user, **data):
    if not user.is_authenticated:
        raise ValidationError("Authentication required.")

    return Car.objects.create(owner=user,**data,)


def update_car(user, car_id, **data):
    car = get_car_for_user(user, car_id)

    for field, value in data.items():
        setattr(car, field, value)

    car.save()

    return car