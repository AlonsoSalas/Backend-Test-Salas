from django.shortcuts import render
from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from users.permissions import IsRegularUser

# Create your views here.


class GenericOrderView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    permission_classes = [IsAuthenticated, IsRegularUser]

    lookup_field = 'id'

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        request.data['user'] = self.request.user.id
        return self.create(request)
