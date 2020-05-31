from django.apps import apps
from django.db import models
import datetime
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist


class OrderQuerySet(models.QuerySet):
    def get_users_orders(self, username):
        return self.filter(user__user__username=username)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def get_users_orders(self, username):
        return self.get_queryset().get_users_orders(username)

    def setDishes(self, dishes, instance):
        order = self.model.objects.get(id=instance.id)
        if dishes:
            Dish = apps.get_model('dishes', 'Dish')
            keep_dishes = []
            for dish in dishes:
                dish_name = dish['name']
                try:
                    dish_instance = Dish.objects.get(
                        name=dish_name, menu=instance.menu)
                except ObjectDoesNotExist:
                    raise NotFound(
                        {'detail': f'There\'s no any dish with the id "{dish_name}" in order menu'})

                keep_dishes.append(dish_instance)

            order.dishes.set(keep_dishes)
        return order
