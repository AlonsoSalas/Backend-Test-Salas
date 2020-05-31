from django.db import models
from dishes.models import Dish
from .managers import MenuManager
from datetime import datetime as dt
import datetime
import os
from rest_framework.exceptions import ValidationError

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField('date published')
    dishes = models.ManyToManyField(Dish)

    objects = MenuManager()

    def __str__(self):
        return self.name

    def isTodayMenu(self):
        today = datetime.date.today()
        return self.date == today

    def isAvailable(self):
        today = datetime.date.today()
        limit_hour = int(os.environ.get('LIMIT_HOUR_TO_ORDER'))
        limit_datetime = dt(
            today.year, today.month, today.day, limit_hour)

        print(dt.now())
        print(limit_datetime)

        if self.isTodayMenu() or dt.now() > limit_datetime:
            raise ValidationError(
                {'detail': f'The menu was avialiable until "{limit_hour}"'})

    class Meta:
        ordering = ['-date']
