from django.urls import path, include
from .views import RegistrationAPIView
from rest_framework.authtoken import views

urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    path('login', views.obtain_auth_token),
]
