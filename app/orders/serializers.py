from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'menu', 'note']
        # fields = '__all__'


# class OrderSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=200)

#     def create(self, validated_data):
#         return Order.objects.create(validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.ingredients = validated_data.get(
#             'ingredients', instance.ingredients)
#         instance.vegetarian = validated_data.get(
#             'vegetarian', instance.vegetarian)
#         instance.nongluten = validated_data.get(
#             'nongluten', instance.nongluten)
#         instance.price = validated_data.get('price', instance.price)
#         instance.save()
#         return instance
