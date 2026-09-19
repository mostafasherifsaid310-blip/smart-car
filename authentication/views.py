from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.http import HttpResponseForbidden
from .utils import is_admin, is_manager,role_required

def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method=="POST":
        form=RegistrationForm(request.POST)

        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect("profile")
    else:
        form=RegistrationForm()

    return render(request,"authentication/register.html",{"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)

        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form=AuthenticationForm()

    return render(request,"authentication/login.html",{"form": form})


@login_required
def profile_view(request):
    return render(request,"authentication/profile.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

# @login_required
# def manager_dashboard(request):

#     if not (is_admin(request.user) or is_manager(request.user)):
#         return HttpResponseForbidden("You do not have permission to access this page.")

#     return render(request,"authentication/manager_dashboard.html")

@login_required
@role_required("Admin", "Manager")
def manager_dashboard(request):

    return render(request,"authentication/manager_dashboard.html")