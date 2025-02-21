from . import views
from django.urls import path

app_name = 'employee'

urlpatterns = [
    path('<user_name>/profile/', views.employee_profile, name="employee_profile"),
    path('<user_name>/profile/update', views.update_employee, name="update_employee"),
    path('all/', views.all_employees, name="all_employees"),
    path('vacation/', views.request_vacation, name="request_vacation"),
    path('vacation/<req_id>/delete/', views.delete_request, name="delete_request"),
    path('vacation/<req_id>/approve/', views.approve_request, name="approve_request"),
    path('vacation/<req_id>/decline/', views.decline_request, name="decline_request"),
    path('messages/<msg_id>/delete/', views.delete_message, name="delete_message"),
    path('messages/<msg_id>/markRead/', views.markRead, name="markRead"),
    path('messages/<msg_id>/unread/', views.unread, name="unread"),
    path('messages/new/', views.send_message, name="send_message"),
]