from django.apps import apps
from django.db import models
import datetime
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist


class OrderQuerySet(models.QuerySet):
    def get_users_orders(self, username):
        return self.filter(user__user__username=username)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def get_users_orders(self, username):
        return self.get_queryset().get_users_orders(username)
