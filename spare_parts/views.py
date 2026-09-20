from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from authentication.utils import is_admin, is_manager
from .forms import SparePartForm
from .models import SparePart


@login_required
def spare_part_list(request):

    parts = SparePart.objects.all().order_by("name")

    return render(request,"spare_parts/spare_part_list.html",{"parts": parts})

@login_required
def spare_part_detail(request, part_id):

    part = get_object_or_404(SparePart,id=part_id)

    return render(request,"spare_parts/spare_part_detail.html",{"part": part})


@login_required
def spare_part_create(request):

    if not is_admin(request.user) and not is_manager(request.user):
        return HttpResponseForbidden("You do not have permission to add spare parts.")

    if request.method == "POST":

        form = SparePartForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("spare_part_list")
    else:
        form = SparePartForm()
        
    return render(
        request,"spare_parts/spare_part_form.html",{"form": form,"title": "Add Spare Part"})

@login_required
def spare_part_update(request, part_id):

    if not is_admin(request.user) and not is_manager(request.user):
        return HttpResponseForbidden("You do not have permission to edit spare parts.")

    part = get_object_or_404(SparePart,id=part_id)

    if request.method == "POST":

        form = SparePartForm(request.POST,instance=part)

        if form.is_valid():

            form.save()

            return redirect("spare_part_detail",part_id=part.id)
    else:

        form = SparePartForm(instance=part)

    return render(request,"spare_parts/spare_part_form.html",{"form": form,"title": "Edit Spare Part"})

@login_required
def spare_part_delete(request, part_id):

    if not is_admin(request.user) and not is_manager(request.user):
        return HttpResponseForbidden(
            "You do not have permission to delete spare parts.")

    part = get_object_or_404(SparePart,id=part_id)

    if request.method == "POST":

        part.delete()

        return redirect("spare_part_list")

    return render(request,"spare_parts/spare_part_confirm_delete.html",{"part": part})