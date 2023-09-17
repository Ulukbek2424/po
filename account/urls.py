from django.urls import path
from .views import WaiterRegistrationView, AdminRegistrationView, WaiterLoginView, AdminLoginView, UserLogoutView


urlpatterns = [
    path('register_waiter/', WaiterRegistrationView.as_view(), name='register_waiter'),
    path('register_admin/', AdminRegistrationView.as_view(), name='register_admin'),
    path('login_waiter/', WaiterLoginView.as_view(), name='login_waiter'),
    path('login_admin/', AdminLoginView.as_view(), name='login_admin'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
