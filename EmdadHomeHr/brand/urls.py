from . import views
from django.urls import path

app_name = 'brand'

urlpatterns = [
    path('<brand_id>/details/', views.brand_details, name='brand_details'),
    path('all/', views.all_brands, name='all_brands'),
    path('add/', views.add_brand, name='add_brand'),
    path('<brand_id>/delete/', views.delete_brand, name='delete_brand'),
    path('<brand_id>/update/', views.update_brand, name='update_brand'),

]