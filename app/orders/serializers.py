from rest_framework import serializers
from dishes.serializers import DishSerializer
from menus.models import Menu
from .models import Order
from .models import Dish
from rest_framework.exceptions import ValidationError, NotFound


class OrderSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'menu', 'dishes', 'note']
        # fields = '__all__'

    def create(self, validated_data):
        menu = validated_data.get('menu')
        if not menu.isAvailable():
            raise ValidationError(
                {'detail': f'The menu {menu.id}" is not Todays menu'})

        dishes = validated_data.pop('dishes')
        validated_dishes = Menu.objects.validateDishes(
            dishes, validated_data.get('menu'))
        if not validated_dishes:
            raise ValidationError(
                {'detail': f'Your order must have at least one dish'})
        order = Order.objects.create(**validated_data)
        order.dishes.set(validated_dishes)
        return order

    def update(self, instance, validated_data):
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        dishes = validated_data.pop('dishes')
        Menu.objects.validateDishes(
            dishes, instance.menu)

        if dishes:
            Order.objects.setDishes(dishes, instance)

        return instance
