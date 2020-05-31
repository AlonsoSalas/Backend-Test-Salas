from django.urls import path, include
from .views import OrderAPIView, OrderDetails, GenericOrderView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('order', GenericOrderView, basename='order')

urlpatterns = [
    # path('', OrderAPIView.as_view()),
    # path('<int:id>/', OrderDetails.as_view()),
    # path('', include(router.urls)),
    # path('<int:pk>/', include(router.urls)),
    path('<int:id>/', GenericOrderView.as_view()),
    path('', GenericOrderView.as_view())

]
