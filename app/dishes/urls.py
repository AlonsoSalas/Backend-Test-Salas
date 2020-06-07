from django.urls import path, include
from .views import DishAPIView

urlpatterns = [
    path('', DishAPIView.as_view()),
    path('<uuid:id>/', DishAPIView.as_view()),
]
