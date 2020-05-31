from django.urls import path, include
from .views import MenuAPIView, MenuDetails, GenericAPIView

urlpatterns = [
    # path('', MenuAPIView.as_view()),
    # path('<int:id>/', MenuDetails.as_view()),
    path('<int:id>/', GenericAPIView.as_view()),
    path('', GenericAPIView.as_view())

]
