from django.urls import path, include
from .views import GenericOrderView


urlpatterns = [

    path('<int:id>/', GenericOrderView.as_view()),
    path('', GenericOrderView.as_view())

]
