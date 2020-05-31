from django.apps import apps
from django.db import models
import datetime
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist


class MenuQuerySet(models.QuerySet):
    def getTodayMenu(self):
        return self.get(date=datetime.date.today())

    def MenuByDate(self, date):
        return self.get(date=date)


class MenuManager(models.Manager):
    def get_queryset(self):
        return MenuQuerySet(self.model, using=self._db)

    def getTodayMenu(self):
        return self.get(date=datetime.date.today())

    def MenuByDate(self, date):
        return self.get(date=date)

    def setDishes(self, dishes, instance):
        menu = self.model.objects.get(id=instance.id)
        if dishes:
            Dish = apps.get_model('dishes', 'Dish')
            keep_dishes = []
            for dish in dishes:
                dish_instance = Dish.objects.get(name=dish['name'])
                keep_dishes.append(dish_instance)

            menu.dishes.set(keep_dishes)
        return menu

    def validateDishes(self, dishes, instance):
        menu = self.model.objects.get(id=instance.id)
        keep_dishes = []
        if dishes:
            Dish = apps.get_model('dishes', 'Dish')
            for dish in dishes:
                dish_name = dish['name']
                try:
                    dish_instance = Dish.objects.get(
                        name=dish_name, menu=menu)
                except ObjectDoesNotExist:
                    raise NotFound(
                        {'detail': f'There\'s no dish with name "{dish_name}" in this menu'})
                keep_dishes.append(dish_instance)
        return keep_dishes
