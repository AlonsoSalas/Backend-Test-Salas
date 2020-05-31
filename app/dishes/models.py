from django.db import models
from .managers import DishManager

# Create your models here.


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    objects = DishManager()

    def __str__(self):
        return self.name
