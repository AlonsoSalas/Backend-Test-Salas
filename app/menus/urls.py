from django.urls import path, include
from .views import GenericMenuAPIView, PublicMenuApiView

urlpatterns = [

    path('<uuid:id>/', GenericMenuAPIView.as_view()),
    path('', GenericMenuAPIView.as_view()),
    path('today', PublicMenuApiView.as_view())
]
