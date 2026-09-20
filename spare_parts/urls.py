from django.urls import path
from .views import (
    spare_part_list,
    spare_part_detail,
    spare_part_create,
    spare_part_update,
    spare_part_delete,)

urlpatterns = [
    path("",spare_part_list,name="spare_part_list"),
    path("add/",spare_part_create,name="spare_part_create"),
    path("<int:part_id>/",spare_part_detail,name="spare_part_detail"),
    path("<int:part_id>/edit/",spare_part_update,name="spare_part_update"),
    path("<int:part_id>/delete/",spare_part_delete,name="spare_part_delete"),]