import pytest
from rest_framework.exceptions import ValidationError
from menus.serializers import MenuSerializer
from menus.models import Menu
from dishes.models import Dish
from datetime import timedelta
import datetime


@pytest.mark.django_db
class TestMenuSerializer:
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    @pytest.mark.parametrize('menu', [
        ({
            "name": "Menu1",
            "date": "2020-08-07",
            "dishes": []
        }),
    ])
    def test_valid_incoming_data(self, menu):
        """
        Should return True when if the data is valid
        """

        serializer = MenuSerializer(data=menu)
        assert serializer.is_valid()

    @pytest.mark.parametrize('menu', [
        ({
            "date": "2020-08-07",
            "dishes": []
        }),
    ])
    def test_invalid_data(self, menu):
        """
        Should raise a ValidationError if the data is not valid
        """

        serializer = MenuSerializer(data=menu)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    @pytest.mark.parametrize('menu_mock', [
        ({
            "name": "Menu1",
            "date": "2019-10-10",
            "dishes": [{
                "name": "Rice with chickexxxn",
                "description": "Awesome flavors mix"
            }]
        }),
    ])
    def test_create(self, mocker, menu_mock):
        """
        Should call Menu.objects.create and validate the dishes if data is valid
        """

        dish = menu_mock['dishes'][0]

        dish = Dish.objects.create(
            name=dish['name'],
            description=dish['description']
        )

        menu_mock['dishes'] = []
        serializer = MenuSerializer(data=menu_mock)

        mocker.patch.object(Dish.objects, 'validate_dishes',
                            return_value=[dish])
        mocker.spy(Menu.objects, 'create')
        mocker.spy(Dish.objects, 'validate_dishes')

        serializer.is_valid(raise_exception=True)
        serializer.save()

        Menu.objects.create.assert_called_once()
        Dish.objects.validate_dishes.assert_called_once()

    @pytest.mark.parametrize('menu_mock', [
        ({
            "name": "Menu1",
            "date": "2019-10-10",
            "dishes": []
        }),
    ])
    def test_update(self, mocker, menu_mock):
        """
        Should call menu.save and retrieve the updated menu
        """

        menu = Menu.objects.create(
            name=menu_mock['name']+'original',
            date=menu_mock['date']
        )

        serializer = MenuSerializer(menu, data=menu_mock)

        mocker.patch.object(Dish.objects, 'validate_dishes',
                            return_value=[])
        mocker.spy(Dish.objects, 'validate_dishes')

        mocker.spy(menu, 'save')
        mocker.spy(menu, 'is_today_menu')

        serializer.is_valid()
        serializer.save()

        menu.refresh_from_db()

        menu.is_today_menu.assert_called_once()
        Dish.objects.validate_dishes.assert_called_once()
        menu.save.assert_called_once()

        assert getattr(menu, 'name') == menu_mock.get('name')
