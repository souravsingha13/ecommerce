from django.urls import path
from .views import RegistrationView,LoginView,LogOutView,ChangePasswordView,VerifyEmail,PasswordResetView, PasswordTokenCheckView


urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogOutView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('forgot-password/', PasswordResetView.as_view(),name="forgot-password"),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', PasswordTokenCheckView.as_view(), name='password-reset-confirm'),

]