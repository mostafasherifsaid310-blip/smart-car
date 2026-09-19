from django.urls import path

from .views import (car_list,car_detail,car_create,car_update,car_delete,)


urlpatterns = [
    path("",car_list,name="car_list"),
    path("add/",car_create,name="car_create"),
    path("<int:car_id>/",car_detail,name="car_detail"),
    path("<int:car_id>/edit/",car_update,name="car_update"),
    path("<int:car_id>/delete/",car_delete,name="car_delete"),]