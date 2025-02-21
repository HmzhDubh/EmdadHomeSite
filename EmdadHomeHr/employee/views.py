from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Employee, VacationRequest, Messages
from datetime import datetime
# Create your views here.


def employee_profile(request: HttpRequest, user_name):
    nationalities = [
        "bangladesh", "egypt", "India", "saudi", "syrian", "yemen"
    ]
    user = User.objects.get(username=user_name)
    if not Employee.objects.filter(user = user).first():
        new_emp_profile = Employee(user=user)
        new_emp_profile.save()

    employee = Employee.objects.get(user=user)

    emp_reqs = VacationRequest.objects.filter(employee = employee)
    msgs = Messages.objects.filter(sender = user)
    return render(request, 'employee_profile.html', context={'emp': employee, 'nationalities': nationalities, 'emp_reqs':emp_reqs, 'msgs': msgs})


def all_employees(request: HttpRequest):

    employees = Employee.objects.all()
    return render(request, 'all_employees.html', context={'employees': employees})


def update_employee(request: HttpRequest, user_name):

    user = User.objects.get(username=user_name)
    employee = Employee.objects.get(user=user)
    try:

        employee.id_num = request.POST['id_num']
        employee.phone_num = request.POST['phone_num']
        employee.about = request.POST['about']
        employee.nationality = request.POST['nationality']
        employee.gender = request.POST['gender']

        employee.user.first_name = request.POST['first_name']
        employee.user.last_name = request.POST['last_name']
        employee.user.last_name = request.POST['last_name']
        employee.save()
        employee.user.save()
        messages.success(request, 'Profile was updated successfully', 'alert-success')
        return redirect('employee:employee_profile', user_name = user.username)
    except Exception as e:
        print(e.__class__)
        messages.error(request, 'Error Updating the Profile', 'alert-danger')
        return redirect('employee:employee_profile', user_name = user.username)


def countDays(date1_str, date2_str):

    date_format = "%Y-%m-%d"
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)

    difference = date2 - date1
    print(difference)

    return difference.days


def request_vacation(request: HttpRequest):

    try:
        if request.method == "POST":

            employee = Employee.objects.get(user=request.user)
            new_vacation = VacationRequest(

                employee = employee,
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'],
                reason = request.POST['reason']

            )
            new_vacation.save()
            # count days
            messages.success(request, f"Your days Vacation Request was sent Successfully", "alert-success")
            return redirect(request.GET.get('next', '/'))

        return render(request, 'request_vacation.html')
    except Exception as e:
        print(e.__class__)
        messages.error(request, "Error in Your Vacation Request Please Try again later", "alert-danger")
        return redirect(request.GET.get('next', '/'))


def delete_request(request: HttpRequest, req_id):

    req = VacationRequest.objects.get(pk=req_id)
    if req.status == 'approved':

        days = countDays(req.start_date.strftime("%Y-%m-%d"), req.end_date.strftime("%Y-%m-%d"))

        req.employee.vacationDays += days
        req.employee.save()

        req.delete()
    else:
        req.delete()
    messages.success(request, f'{req.employee.id_num} Vacation Request Has Been Deleted Successfully', 'alert-success')
    return redirect('employee:employee_profile', user_name = req.employee.user.username)


def approve_request(request: HttpRequest, req_id):

    req = VacationRequest.objects.get(pk=req_id)

    days = countDays(req.start_date.strftime("%Y-%m-%d"), req.end_date.strftime("%Y-%m-%d"))
    if days <= 0 or days > req.employee.vacationDays:

        req.status = 'declined'
        req.save()

        messages.error(request, f'{req.employee.id_num} Does Not have Enough Vacation Days', 'alert-danger')
        return redirect('employee:employee_profile', user_name = req.employee.user.username)

    req.status = 'approved'
    req.save()

    req.employee.vacationDays -= days
    req.employee.save()

    messages.success(request, f'{req.employee.id_num} Vacation Request Has Been Approved Successfully', 'alert-success')
    return redirect('employee:employee_profile', user_name = req.employee.user.username)


def decline_request(request: HttpRequest, req_id):

    req = VacationRequest.objects.get(pk=req_id)
    req.status = 'declined'
    req.save()
    messages.success(request, f'{req.employee.id_num} Vacation Request Has Been Declined', 'alert-warning')
    return redirect('employee:employee_profile', user_name = req.employee.user.username)


def send_message(request: HttpRequest):
    if request.method == "POST":
        new_message = Messages(
            sender = request.user,
            subject = request.POST['subject'],
            content = request.POST['content'],
        )
        new_message.save()
        messages.success(request, 'Your Message was sent successfully', 'alert-success')
    return redirect('HrApp:home_view')


def delete_message(request: HttpRequest, msg_id):

    msg = Messages.objects.get(pk=msg_id)
    msg.delete()
    messages.success(request, f'{msg.sender.first_name} {msg.sender.last_name} Message Has Been Deleted Successfully', 'alert-success')
    return redirect('employee:employee_profile', user_name = msg.sender.username)


def markRead(request: HttpRequest, msg_id):
    msg = Messages.objects.get(pk=msg_id)
    msg.is_viewed = True
    msg.save()
    messages.success(request, f'{msg.sender.first_name} {msg.sender.last_name} Message Has Been Marked as Read Successfully', 'alert-success')
    return redirect('employee:employee_profile', user_name = msg.sender.username)


def unread(request: HttpRequest, msg_id):
    msg = Messages.objects.get(pk=msg_id)
    msg.is_viewed = False
    msg.save()
    messages.success(request, f'{msg.sender.first_name} {msg.sender.last_name} Message Has Been Unread Successfully', 'alert-warning')
    return redirect('employee:employee_profile', user_name = msg.sender.username)

