from django.db import models
from django.conf import settings
from menus.models import Menu
from dishes.models import Dish
from .managers import OrderManager
import uuid
# Create your models here.


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=250)
    dishes = models.ManyToManyField(Dish)

    objects = OrderManager()

    def __str__(self):
        return str(self.pk)
