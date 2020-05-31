from django.urls import path, include
from .views import DishAPIView, DishDetails

urlpatterns = [
    path('', DishAPIView.as_view()),
    path('<int:id>/', DishDetails.as_view()),
]