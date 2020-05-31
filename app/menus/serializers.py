from rest_framework import serializers
from dishes.serializers import DishSerializer
from .models import Menu
from dishes.models import Dish
from rest_framework.validators import UniqueValidator
import datetime
import logging

logger = logging.getLogger(__name__)


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)
    date = serializers.DateField(
        validators=[UniqueValidator(queryset=Menu.objects.all(), message="There is already a menu for that date.")])

    class Meta:
        model = Menu
        fields = ['id', 'name', 'date', 'dishes']

    def create(self, validated_data):
        dishes = validated_data.pop('dishes')
        menu = Menu.objects.create(**validated_data)
        if dishes:
            Menu.objects.setDishes(dishes, menu)
        return menu

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        if not instance.isTodayMenu():
            instance.date = validated_data.get('date', instance.date)

        instance.save()

        dishes = validated_data.pop('dishes')

        if dishes:
            Menu.objects.setDishes(dishes, instance)

        return instance
