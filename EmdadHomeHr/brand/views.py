from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Brand
# Create your views here.


def all_brands(request: HttpRequest):

    brands = Brand.objects.all()

    return render(request, 'all_brands.html', context={'brands': brands})


def brand_details(request: HttpRequest, brand_id):
    brand = Brand.objects.get(pk = brand_id)
    return render(request, 'brand_details.html', context={'brand': brand})


def add_brand(request: HttpRequest):

    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Only Authorized users Can Add Brands", 'alert-danger')
        return redirect('accounts:login_view')
    try:

        if request.method == "POST":

            new_brand = Brand(
                name = request.POST['name'],
                about = request.POST['about'],
                logo = request.FILES.get("logo", Brand._meta.get_field("logo").get_default()),
            )

            new_brand.save()
            messages.success(request, 'Brand Was Added Successfully')
            return render(request, 'all_brands.html')
        return render(request, 'add_brand.html')
    except Exception as e:
        print(e)
        messages.error(request, 'Error While Adding Brand, Please Try Again Later')
        return render(request, 'home.html')




def delete_brand(request: HttpRequest, brand_id):

    if request.user.is_authenticated and request.user.is_staff:
        brand = Brand.objects.get(pk=brand_id)
        brand.delete()

    messages.warning(request, 'message was deleted Successfully', 'alert-warning')
    return redirect('brand:all_brands')


def update_brand(request: HttpRequest,brand_id):

    if not (request.user.is_staff or request.user.is_authenticated):
        messages.error(request, "Only Authorized Uses Can update Brands", 'alert-danger')
        return redirect('brand:brand_details', brand_id=brand_id)

    try:

        brand = Brand.objects.get(pk=brand_id)

        if request.method == "POST":
            with transaction.atomic():
                brand.name = request.POST['name']
                brand.about = request.POST['about']

                if 'logo' in request.FILES: brand.logo = request.FILES['logo']

                brand.save()

                messages.success(request, "Brand was Updated successfully", "alert-success")
                return redirect("brand:brand_details", brand_id = brand_id)

        return render(request, 'update_brand.html', context={'brand':brand})

    except Exception as e:

        print(e)
        messages.error(request, "Error adding fund", "alert-danger")
        return redirect(request, 'brand:all_brands')