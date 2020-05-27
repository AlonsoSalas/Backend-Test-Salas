from django.db import models
from dishes.models import Dish

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField('date published')
    dishes = models.ManyToManyField(Dish)

    def __str__(self):
        return self.name
