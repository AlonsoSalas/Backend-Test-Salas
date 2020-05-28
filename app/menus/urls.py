from django.urls import path, include
from .views import MenuAPIView, MenuDetails

urlpatterns = [
    path('', MenuAPIView.as_view()),
    path('<int:id>/', MenuDetails.as_view()),
]
