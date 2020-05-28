from django.urls import path, include
from .views import OrderAPIView, OrderDetails

urlpatterns = [
    path('', OrderAPIView.as_view()),
    path('<int:id>/', OrderDetails.as_view()),
]
