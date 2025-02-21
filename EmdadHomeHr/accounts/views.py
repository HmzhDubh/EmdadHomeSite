from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from employee.models import Employee


# Create your views here.


def register_view(request: HttpRequest):

    if request.method == "POST" and request.POST['password'] == request.POST['v_password']:
        try:
            with transaction.atomic():
                new_user = User.objects.create_user(

                    username = request.POST['email'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    password = request.POST['password'],
                    email = request.POST['email'],
                )
                new_user.save()
                emp = Employee(
                    user = new_user,
                    id_num = request.POST['id_num'],
                    gender = request.POST['gender'],
                    avatar = request.FILES.get("avatar", Employee._meta.get_field("avatar").get_default()),
                )

                emp.save()

            login(request, new_user)
            messages.success(request, f'{new_user.username} Account was created Successfully', 'alert-success')

            return redirect("HrApp:home_view")
        except IntegrityError as ie:
            print(ie)
            messages.error(request, 'This email is already registered, please try another one or login directly', 'alert-danger')
        except Exception as e:
            print(e.__class__)
            messages.error(request, 'error in creating your account', 'alert-danger')

    return render(request, 'register.html')


def login_view(request: HttpRequest):

    if request.method == "POST":
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, f'{user.username} Signed in Successfully', 'alert-success')
            return redirect("HrApp:home_view")
        else:
            messages.error(request, 'Email or password is wrong, please try again', 'alert-danger')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Log Out Successfully", 'alert-success')
    return redirect('HrApp:home_view')

