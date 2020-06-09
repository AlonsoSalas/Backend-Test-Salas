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

        validated_dishes = Dish.objects.validate_dishes(dishes)
        if validated_dishes:
            menu.dishes.set(validated_dishes)

        return menu

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        dishes = validated_data.pop('dishes')

        if not instance.is_today_menu():
            instance.date = validated_data.get('date', instance.date)
        instance.save()

        validated_dishes = Dish.objects.validate_dishes(dishes)
        if validated_dishes:
            instance.dishes.set(validated_dishes)

        return instance
