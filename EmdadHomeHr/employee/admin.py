from django.contrib import admin
from .models import Employee, VacationRequest, Messages
# Register your models here.

admin.site.register(Employee)
admin.site.register(VacationRequest)
admin.site.register(Messages)