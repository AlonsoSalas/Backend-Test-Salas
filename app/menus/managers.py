from django.apps import apps
from django.db import models
import datetime
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist


class MenuManager(models.Manager):
    """
    Menu Manager.
    """

    def get_today_menu(self):
        """
        Get Todays Menu

        Raises:
            NotFound: [If there is no Menu for today]
        """
        try:
            menu = self.get(date=datetime.date.today())
            return menu
        except ObjectDoesNotExist:
            raise NotFound(
                {'detail': 'There\'s no menu for today'})
