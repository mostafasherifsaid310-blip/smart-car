from django.urls import path
from .views import (register_view,login_view,profile_view,logout_view, manager_dashboard,)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("profile/", profile_view, name="profile"),
    path("logout/", logout_view, name="logout"),
    path("manager/",manager_dashboard,name="manager_dashboard"),]