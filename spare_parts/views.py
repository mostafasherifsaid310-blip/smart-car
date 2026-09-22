# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from django.shortcuts import get_object_or_404, redirect, render
# from authentication.utils import is_admin, is_manager
# from .forms import SparePartForm
# from .models import SparePart
# from django.db.models.deletion import ProtectedError


# def management_access_required(user):
#     return is_admin(user) or is_manager(user)


# @login_required
# def spare_part_list(request):

#     if not management_access_required(request.user):
#         return HttpResponseForbidden(
#             "You do not have permission to manage spare parts.")

#     spare_parts = SparePart.objects.all().order_by("name")

#     return render(request,
#         "spare_parts/spare_part_list.html",
#         {"spare_parts": spare_parts,},)


# @login_required
# def spare_part_detail(request, spare_part_id):

#     if not management_access_required(request.user):
#         return HttpResponseForbidden(
#             "You do not have permission to view spare parts.")

#     spare_part = get_object_or_404(SparePart,id=spare_part_id,)

#     return render(request,
#         "spare_parts/spare_part_detail.html",
#         {"spare_part": spare_part,},)

# @login_required
# def spare_part_create(request):

#     if not management_access_required(request.user):
#         return HttpResponseForbidden(
#             "You do not have permission to create spare parts."
#         )

#     if request.method == "POST":

#         form = SparePartForm(request.POST)

#         if form.is_valid():
#             form.save()

#             return redirect("spare_part_list")

#     else:
#         form = SparePartForm()

#     return render(request,
#         "spare_parts/spare_part_form.html",
#         {"form": form,"title": "Add Spare Part",},)


# @login_required
# def spare_part_update(request, spare_part_id):

#     if not management_access_required(request.user):
#         return HttpResponseForbidden(
#             "You do not have permission to edit spare parts.")

#     spare_part = get_object_or_404(SparePart,id=spare_part_id,)

#     if request.method == "POST":

#         form = SparePartForm(request.POST,instance=spare_part,)

#         if form.is_valid():
#             form.save()

#             return redirect("spare_part_detail",spare_part_id=spare_part.id,)

#     else:
#         form = SparePartForm(instance=spare_part,)

#     return render(request,
#         "spare_parts/spare_part_form.html",
#         {"form": form,"title": "Edit Spare Part",},)


# @login_required
# def spare_part_delete(request, spare_part_id):
#     if not management_access_required(request.user):
#         return HttpResponseForbidden("You do not have permission to delete spare parts.")

#     spare_part = get_object_or_404(SparePart, id=spare_part_id)

#     if request.method == "POST":
#         try:
#             spare_part.delete()
#             return redirect("spare_part_list")

#         except ProtectedError:
#             return render(request,
#                 "spare_parts/spare_part_confirm_delete.html",
#                 {"spare_part": spare_part,
#                     "delete_error": ("This spare part cannot be deleted because "
#                         "it is linked to existing maintenance records."),},status=400,)

#     return render(request,"spare_parts/spare_part_confirm_delete.html",{"spare_part": spare_part},)

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from authentication.utils import is_admin, is_manager

from .forms import SparePartForm
from .services import (
    get_all_spare_parts,
    get_spare_part,
    create_spare_part,
)


def management_access_required(user):
    return is_admin(user) or is_manager(user)


@login_required
def spare_part_list(request):
    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to manage spare parts."
        )

    spare_parts = get_all_spare_parts()

    return render(
        request,
        "spare_parts/spare_part_list.html",
        {
            "spare_parts": spare_parts,
        },
    )


@login_required
def spare_part_detail(request, spare_part_id):
    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to view spare parts."
        )

    try:
        spare_part = get_spare_part(spare_part_id)
    except ValidationError as error:
        return HttpResponseForbidden(error.message)

    return render(
        request,
        "spare_parts/spare_part_detail.html",
        {
            "spare_part": spare_part,
        },
    )


@login_required
def spare_part_create(request):
    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to create spare parts."
        )

    if request.method == "POST":
        form = SparePartForm(request.POST)

        if form.is_valid():
            data = {
                field: form.cleaned_data[field]
                for field in form.fields
            }

            try:
                create_spare_part(**data)

                return redirect("spare_part_list")

            except ValidationError as error:
                form.add_error(None, error.message)

    else:
        form = SparePartForm()

    return render(
        request,
        "spare_parts/spare_part_form.html",
        {
            "form": form,
            "title": "Add Spare Part",
        },
    )


@login_required
def spare_part_update(request, spare_part_id):
    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to edit spare parts."
        )

    try:
        spare_part = get_spare_part(spare_part_id)
    except ValidationError as error:
        return HttpResponseForbidden(error.message)

    if request.method == "POST":
        form = SparePartForm(
            request.POST,
            instance=spare_part,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "spare_part_detail",
                spare_part_id=spare_part.id,
            )

    else:
        form = SparePartForm(
            instance=spare_part
        )

    return render(
        request,
        "spare_parts/spare_part_form.html",
        {
            "form": form,
            "title": "Edit Spare Part",
        },
    )


@login_required
def spare_part_delete(request, spare_part_id):
    if not management_access_required(request.user):
        return HttpResponseForbidden(
            "You do not have permission to delete spare parts."
        )

    try:
        spare_part = get_spare_part(spare_part_id)
    except ValidationError as error:
        return HttpResponseForbidden(error.message)

    if request.method == "POST":
        try:
            spare_part.delete()

            return redirect("spare_part_list")

        except ProtectedError:
            return render(
                request,
                "spare_parts/spare_part_confirm_delete.html",
                {
                    "spare_part": spare_part,
                    "delete_error": (
                        "This spare part cannot be deleted because "
                        "it is linked to existing maintenance records."
                    ),
                },
                status=400,
            )

    return render(
        request,
        "spare_parts/spare_part_confirm_delete.html",
        {
            "spare_part": spare_part,
        },
    )