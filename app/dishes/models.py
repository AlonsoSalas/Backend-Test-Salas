from django.db import models
from .managers import DishManager
from common.models import BaseModel
import uuid

# Create your models here.


class Dish(BaseModel):
    """
    Dish model class
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    objects = DishManager()

    def __str__(self):
        return self.name
