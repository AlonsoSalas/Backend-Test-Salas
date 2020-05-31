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
# Create your views here.


class OrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        menus = Order.objects.all()
        serializer = OrderSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetails(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Order.objects.get(id=id)

        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        menu = self.get_object(id)
        serializer = OrderSerializer(menu)
        return Response(serializer.data)

    def put(self, request, id):
        menu = self.get_object(id)
        serializer = OrderSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        menu = self.get_object(id)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenericOrderView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)
