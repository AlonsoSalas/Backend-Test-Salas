from django.shortcuts import render
from .models import Dish
from .serializers import DishSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.


class DishAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        menus = Dish.objects.all()
        serializer = DishSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetails(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, id):
        try:
            return Dish.objects.get(id=id)

        except Dish.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        menu = self.get_object(id)
        serializer = DishSerializer(menu)
        return Response(serializer.data)

    def put(self, request, id):
        menu = self.get_object(id)
        serializer = DishSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        menu = self.get_object(id)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
