from django.db import models
from dishes.models import Dish
from .managers import MenuManager
from datetime import datetime as dt
from common.models import BaseModel
import datetime
import os
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localdate
import uuid

# Create your models here.


class Menu(BaseModel):
    """
    Menu model class
    """
    name = models.CharField(max_length=100)
    date = models.DateField('date published')
    dishes = models.ManyToManyField(Dish)

    objects = MenuManager()

    def __str__(self):
        return self.name

    def is_today_menu(self) -> bool:
        """
        [Determines whether or not the instance menu is todays menus]
        """
        today = datetime.date.today()
        return self.date == today

    def is_available(self):
        """
        [Determines whether or not the instance menu is available to take orders]

        Raises:
            NotFound: [ If the hour limit has passed ]
        """
        today = datetime.date.today()
        limit_hour = int(os.environ.get('LIMIT_HOUR_TO_ORDER'))
        limit_datetime = dt(
            today.year, today.month, today.day, limit_hour)

        if dt.now() > limit_datetime:
            raise NotFound(
                {'detail': f'The menu was avialiable until "{limit_hour}"'})
        pass

    def validate_dishes_belonging(self, dishes):
        """
        [Determines whether or not the dishes belongs to instance menu ]

        Arguments:
            dishes [Dishes] -- [Dish objects array to be validated with the menu instance]

        Raises:
            NotFound: [ If one of those dishes doesn't belong to the menu instance]
        """
        validatedDishes = []
        if dishes:
            for dish in dishes:
                dish_name = dish['name']
                try:
                    dish_instance = self.dishes.get(
                        name=dish_name)
                except ObjectDoesNotExist:
                    raise NotFound(
                        {'detail': f'There\'s no dish with name "{dish_name}" in today`s Menu'})
                validatedDishes.append(dish_instance)
        return validatedDishes

    class Meta:
        ordering = ['-date']
