from django.urls import path, include
from .views import GenericMenuAPIView

urlpatterns = [

    path('<int:id>/', GenericMenuAPIView.as_view()),
    path('', GenericMenuAPIView.as_view())

]
