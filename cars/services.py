from django.core.exceptions import ValidationError
from .models import Car

def get_user_cars(user):
    return Car.objects.filter(owner=user).order_by("-created_at")


# def get_car_for_user(user, car_id):
#     try:
#         car = Car.objects.get(id=car_id)
#     except Car.DoesNotExist:
#         raise ValidationError("Car not found.")

#     if car.owner != user:
#         raise ValidationError("You do not have permission to access this car.")

#     return car

def get_car_for_user(user, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise ValidationError("Car not found.")

    is_staff_role = user.groups.filter(
        name__in=["Admin", "Manager"]
    ).exists()

    if not is_staff_role and car.owner != user:
        raise ValidationError(
            "You do not have permission to access this car."
        )

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

def get_my_cars(user):
    if not user or not user.is_authenticated:
        raise ValidationError("Authentication required.")

    cars = Car.objects.filter(owner=user).order_by("-created_at")

    return {
        "cars": [
            {
                "id": car.id,
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "license_plate": car.license_plate,
                "mileage": car.mileage,
                "color": car.color,
            }
            for car in cars
        ]
    }
    
