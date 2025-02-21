from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_num = models.CharField(max_length=10)
    phone_num = models.CharField(max_length=10, default='None')
    nationality = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    about = models.TextField(null=True)
    vacationDays = models.SmallIntegerField(default=21)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='images/avatars', default='images/avatars/profileAvatar.jpg')

    def __str__(self):
        return f"Employee: {self.user.first_name}{self.user.last_name} Profile"


class VacationRequest(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.TextField(default="None")
    status = models.CharField(max_length=20, default='pending')


class Messages(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=1024, blank=True)
    content = models.TextField()
    is_viewed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"from: {self.sender} at {self.sent_at}"


