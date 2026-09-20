from django.urls import path

from .views import (
    technician_list,
    technician_detail,
    technician_create,
    technician_update,
    technician_delete,)


urlpatterns = [
    path("",technician_list,name="technician_list",),
    path("add/",technician_create,name="technician_create",),
    path("<int:technician_id>/",technician_detail,name="technician_detail",),
    path("<int:technician_id>/edit/",technician_update,name="technician_update",),
    path("<int:technician_id>/delete/",technician_delete,name="technician_delete",),]