from django.urls import path
from .views import RegistrationView,LoginView,LogOutView,ChangePasswordView


urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),

]