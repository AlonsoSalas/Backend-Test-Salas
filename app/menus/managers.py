from django.apps import apps
from django.db import models
import datetime
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist


class MenuManager(models.Manager):
    def getTodayMenu(self):
        try:
            menu = self.get(date=datetime.date.today())
            return menu
        except ObjectDoesNotExist:
            raise NotFound(
                {'detail': 'There\'s no menu for today'})
