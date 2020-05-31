from django.apps import apps
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, NotFound


class DishManager(models.Manager):

    def validateDishes(self, dishes):
        keep_dishes = []
        if dishes:
            for dish in dishes:
                dish_name = dish['name']
                try:
                    dish_instance = self.get(
                        name=dish_name)
                except ObjectDoesNotExist:
                    raise NotFound(
                        {'detail': f'There\'s no dish with name "{dish_name}"'})
                keep_dishes.append(dish_instance)
        return keep_dishes
