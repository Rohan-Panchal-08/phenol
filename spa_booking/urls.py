from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from bookings import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('get-booked-slots/', views.get_booked_slots, name='get_booked_slots'),
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')),

]
