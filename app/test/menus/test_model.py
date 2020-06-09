import pytest
import os
from rest_framework.exceptions import NotFound
from datetime import date
from menus.models import Menu
from dishes.models import Dish


@pytest.mark.django_db
class TestMenuModel:
    @pytest.mark.parametrize('menu', [
        ({'name': 'Italian Menu',
            'date': date.today()})
    ])
    def test_is_today_menu(self, menu):
        """
        Should return True if the menu is todays menu
        """
        menu = Menu.objects.create(**menu)
        assert menu.is_today_menu()

    @pytest.mark.parametrize('menu', [
        ({'name': 'Italian Menu',
            'date': '2019-01-01'})
    ])
    def test_is_not_today_menu(self, menu):
        """
        Should return False if the menu is not todays menu
        """
        menu = Menu.objects.create(**menu)
        assert menu.is_today_menu() != True

    @pytest.mark.parametrize('menu', [
        ({'name': 'Italian Menu',
            'date': date.today()})
    ])
    def test_is_available(self, mocker,  menu):
        """
        Should return none because if is available it simply pass
        """
        mocker.patch.dict(os.environ, {'LIMIT_HOUR_TO_ORDER': '23'})

        menu = Menu.objects.create(**menu)
        assert menu.is_available() == None

    @pytest.mark.parametrize('menu', [
        ({'name': 'Italian Menu',
            'date': date.today()})
    ])
    def test_is_not_available(self, mocker, menu):
        """
        Should raise an error if the menu is not available
        """
        mocker.patch.dict(os.environ, {'LIMIT_HOUR_TO_ORDER': '1'})

        menu = Menu.objects.create(**menu)
        with pytest.raises(NotFound):
            menu.is_available()

    @pytest.mark.parametrize('menu', [
        ({'name': 'Italian Menu',
            'date': date.today()})
    ])
    @pytest.mark.parametrize('dishes', [
        ([{'name': 'Lasagna',
           'description': 'Italian Dish'},
          {'name': 'Sushi',
            'description': 'Japaneese Dish'}]),
    ])
    def test_validate_dishes_belonging(self, menu, dishes):
        """
        Should return the validated dishes when they are associated to the menu
        """
        menu = Menu.objects.create(**menu)
        dishes_instances = []
        for dish in dishes:
            dish = Dish.objects.create(**dish)
            dishes_instances.append(dish)

        menu.dishes.set(dishes_instances)

        validatedDishes = menu.validate_dishes_belonging(dishes)
        assert len(validatedDishes) == len(dishes)

    @pytest.mark.parametrize('menu', [
        ({'name': 'Italian Menu',
            'date': date.today()})
    ])
    @pytest.mark.parametrize('dishes', [
        ([{'name': 'Lasagna',
           'description': 'Italian Dish'},
          {'name': 'Sushi',
            'description': 'Japaneese Dish'}]),
    ])
    def test_not_validate_dishes_belonging(self, menu, dishes):
        """
        Should return error if the dishes are not associated to the user
        """
        menu = Menu.objects.create(**menu)
        dishes_instances = []
        for dish in dishes:
            dish = Dish.objects.create(**dish)
            dishes_instances.append(dish)

        with pytest.raises(NotFound):
            menu.validate_dishes_belonging(dishes)


2
