from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from brand.models import Brand
from employee.models import Employee
from django.contrib.auth.models import User
# Create your views here.


def home_view(request: HttpRequest):

    brands = Brand.objects.all()[:4]
    employees = Employee.objects.all()[:4]

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
    print("Superuser created successfully.")

    return render(request, 'home.html', context={
        'brands': brands,
        'employees': employees
    })


def search_view(request: HttpRequest):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        brands = Brand.objects.filter(
            Q(name__contains=keyword) |
            Q(about__contains=keyword)
        )
    else:
        brands = []

    return render(request, 'search_results.html', context={'brands':brands})
