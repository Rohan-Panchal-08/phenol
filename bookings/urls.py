from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_form, name='booking_form'),
    path('export/', views.export_excel, name='export_excel'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/booking-count/', views.get_booking_count, name='booking_count'),
]
