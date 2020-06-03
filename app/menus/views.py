from django.shortcuts import render
from .models import Menu
from .serializers import MenuSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .permissions import isTodayMenu
# Create your views here.


class GenericMenuAPIView(generics.GenericAPIView, mixins.ListModelMixin,
                         mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

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


class PublicMenuApiView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    lookup_field = 'id'
    permission_classes = [isTodayMenu]

    def get(self, request, id=None):
        return self.retrieve(request)
