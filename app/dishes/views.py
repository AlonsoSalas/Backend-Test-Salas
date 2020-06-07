from django.shortcuts import render
from .models import Dish
from .serializers import DishSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.


class DishAPIView(generics.GenericAPIView, mixins.ListModelMixin,
                  mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


# class DishDetails(APIView):

#     permission_classes = [IsAuthenticated, IsAdminUser]

#     def get_object(self, id):
#         try:
#             return Dish.objects.get(id=id)

#         except Dish.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, id):
#         menu = self.get_object(id)
#         serializer = DishSerializer(menu)
#         return Response(serializer.data)

#     def put(self, request, id):
#         menu = self.get_object(id)
#         serializer = DishSerializer(menu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         menu = self.get_object(id)
#         menu.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
