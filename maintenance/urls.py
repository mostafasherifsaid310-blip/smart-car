from django.urls import path
from .views import (
    maintenance_list,
    maintenance_detail,
    maintenance_create,
    maintenance_update,
    maintenance_delete,
    maintenance_add_part,
    maintenance_remove_part,)


urlpatterns = [
    path("",maintenance_list,name="maintenance_list"),
    path("add/",maintenance_create,name="maintenance_create"),
    path("<int:maintenance_id>/",maintenance_detail,name="maintenance_detail"),
    path("<int:maintenance_id>/edit/",maintenance_update,name="maintenance_update"),
    path("<int:maintenance_id>/delete/",maintenance_delete,name="maintenance_delete"),
    path("<int:maintenance_id>/add-part/",maintenance_add_part,name="maintenance_add_part"),
    path("part/<int:maintenance_part_id>/remove/",maintenance_remove_part,name="maintenance_remove_part"),]