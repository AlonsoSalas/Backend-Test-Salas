from django.db import models
from .managers import DishManager
import uuid

# Create your models here.


class Dish(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    objects = DishManager()

    def __str__(self):
        return self.name
