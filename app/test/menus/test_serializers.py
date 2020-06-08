import pytest
from rest_framework.exceptions import ValidationError
from menus.serializers import MenuSerializer
from menus.models import Menu
from dishes.models import Dish
from uuid import uuid4
from datetime import date, timedelta
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
        Should return True when the incoming data is valid
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
        Should raise a ValidationError when the incoming data is not valid
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
        Should raise a ValidationError when the incoming data is not valid
        """

        dish = menu_mock['dishes'][0]

        dish = Dish.objects.create(
            name=dish['name'],
            description=dish['description']
        )

        menu_mock['dishes'] = []
        serializer = MenuSerializer(data=menu_mock)

        mocker.patch.object(Dish.objects, 'validateDishes',
                            return_value=[dish])
        mocker.spy(Menu.objects, 'create')
        mocker.spy(Dish.objects, 'validateDishes')

        serializer.is_valid(raise_exception=True)
        serializer.save()

        Menu.objects.create.assert_called_once()
        Dish.objects.validateDishes.assert_called_once()

    @pytest.mark.parametrize('menu_mock', [
        ({
            "name": "Menu1",
            "date": "2019-10-10",
            "dishes": []
        }),
    ])
    def test_update(self, mocker, menu_mock):
        """
        Should call instance.save() method and update the instance 
        """

        menu = Menu.objects.create(
            name=menu_mock['name']+'original',
            date=menu_mock['date']
        )

        serializer = MenuSerializer(menu, data=menu_mock)

        mocker.patch.object(Dish.objects, 'validateDishes',
                            return_value=[])
        mocker.spy(Dish.objects, 'validateDishes')

        mocker.spy(menu, 'save')
        mocker.spy(menu, 'isTodayMenu')

        serializer.is_valid()
        serializer.save()

        menu.refresh_from_db()

        menu.isTodayMenu.assert_called_once()
        Dish.objects.validateDishes.assert_called_once()
        menu.save.assert_called_once()

        assert getattr(menu, 'name') == menu_mock.get('name')
