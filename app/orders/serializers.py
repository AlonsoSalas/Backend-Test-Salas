from rest_framework import serializers
from dishes.serializers import DishSerializer
from menus.models import Menu
from .models import Order
from .models import Dish
from rest_framework.exceptions import ValidationError, NotFound


class OrderSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    note = serializers.CharField(allow_blank=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'menu', 'dishes', 'note']

    def validate(self, data):
        """
        Validates that dishes nested objects len is more than one, and also validate if they belongs to todays menu
        """
        dishes = data['dishes']
        if not dishes:
            raise serializers.ValidationError(
                "Your order must have at least one dish")
        menu = data['menu']
        data['dishes'] = menu.validate_dishes_belonging(
            dishes)
        data['user'] = self.context['user']

        return data

    def create(self, validated_data):
        menu = validated_data.get('menu')
        if not menu.is_today_menu():
            raise ValidationError(
                {'detail': f'The menu {menu.id}" is not Todays menu'})

        menu.is_available()

        dishes = validated_data.pop('dishes')

        order = Order.objects.create(**validated_data)
        order.dishes.set(dishes)
        return order

    def update(self, instance, validated_data):
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        dishes = validated_data.pop('dishes')
        instance.dishes.set(dishes)

        return instance
