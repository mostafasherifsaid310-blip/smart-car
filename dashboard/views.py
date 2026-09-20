from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from authentication.utils import is_admin, is_manager
from .services import get_dashboard_data


@login_required
def dashboard_view(request):

    is_manager_or_admin = (is_admin(request.user)or is_manager(request.user))

    dashboard_data = get_dashboard_data(user=request.user,
        is_manager_or_admin=is_manager_or_admin,)

    context = {**dashboard_data,"is_manager_or_admin": is_manager_or_admin,}

    return render(request,"dashboard/dashboard.html",context,)