from django.urls import path, include
from .views import GenericOrderView


urlpatterns = [

    path('<uuid:id>/', GenericOrderView.as_view()),
    path('', GenericOrderView.as_view())

]
