from django.db import models
from users.models import CustomUser
from menus.models import Menu

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    menus = models.ManyToManyField(Menu)
    note = models.CharField(max_length=250)

    def __str__(self):
        return self.totalPrice
