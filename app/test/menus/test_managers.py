import pytest
from rest_framework.exceptions import ValidationError, NotFound
from menus.models import Menu
from datetime import date
import datetime
# from ..helpers import get_future_day
from uuid import uuid4


@pytest.mark.django_db
class TestMenuManager:
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    @pytest.mark.parametrize('menus', [
        ([{'name': 'Italian Menu',
            'date': date.today()},
          {'name': 'Japanesse Menu',
            'date': tomorrow}]),
    ])
    def test_getTodayMenu(self, menus):
        """
        Should return Dishes the 2 dishes that are already created
        """
        for menu in menus:
            Menu.objects.create(**menu)
        todayMenu = Menu.objects.getTodayMenu()

        assert todayMenu.name == menus[0]['name']

    def test_not_getTodayMenu(self):
        """
        Should return Dishes the 2 dishes that are already created
        """
        with pytest.raises(NotFound):
            Menu.objects.getTodayMenu()
