from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify-otp/', views.OTPVerifyView.as_view()),
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('profile/', views.ProfileCreateUpdateView.as_view()),  # get / patch
    path('forgot-password/', views.ForgotPasswordView.as_view()),
    path('reset-password/', views.ResetPasswordView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
