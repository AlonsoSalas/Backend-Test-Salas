import pytest
from rest_framework.exceptions import NotFound
from menus.models import Menu
from datetime import date
import datetime


@pytest.mark.django_db
class TestMenuManager:
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    @pytest.mark.parametrize('menus', [
        ([{'name': 'Italian Menu',
            'date': date.today()},
          {'name': 'Japanesse Menu',
            'date': tomorrow}]),
    ])
    def test_get_today_menu(self, menus):
        """
        Should return the first menu
        """
        for menu in menus:
            Menu.objects.create(**menu)
        todayMenu = Menu.objects.get_today_menu()

        assert todayMenu.name == menus[0]['name']

    def test_not_get_today_menu(self):
        """
        Should raises a NotFound error when there is not menu today
        """
        with pytest.raises(NotFound):
            Menu.objects.get_today_menu()
