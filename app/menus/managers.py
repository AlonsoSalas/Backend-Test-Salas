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
        try:
            menu = self.get(date=datetime.date.today())
            menu.isAvailable()
            return menu
        except ObjectDoesNotExist:
            raise NotFound(
                {'detail': 'There\'s no menu for today'})

    def MenuByDate(self, date):
        return self.get(date=date)
