import pytest
import os
from rest_framework.exceptions import ValidationError
from orders.serializers import OrderSerializer
from orders.models import Order
from dishes.models import Dish
from menus.models import Menu
from test.helper import AuthAPIRequestFactory
from uuid import uuid4
from datetime import date, timedelta
import datetime


@pytest.mark.django_db
class TestOrderSerializer:
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    def test_valid_incoming_data(self, super_user, mocker):
        """
        Should return True when the incoming data is valid
        """
        dish = Dish.objects.create(
            name="Lasagna",
            description="very great italian lasagna"
        )
        menu = Menu.objects.create(
            name="Menu 1",
            date=datetime.date.today()
        )
        menu.dishes.set([dish])

        mock_order = {
            "menu": str(menu.id),
            "dishes": [
                {
                    'name': "Lasagna",
                    'description': "very great italian lasagna"
                }
            ],
            "note": "spicy plz",
            "user": ""
        }

        mocker.patch.object(Order.objects, 'get',
                            return_value=dish)

        serializer = OrderSerializer(context={'user': super_user},
                                     data=mock_order)
        serializer.is_valid(raise_exception=True)
        assert serializer.is_valid()

    def test_invalid_data(self):
        """
        Should raise a ValidationError when the incoming data is not valid
        """
        mock_order = {
            "menu": '123',
            "dishes": [
            ],
            "note": "spicy plz"
        }
        serializer = OrderSerializer(data=mock_order)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create(self, super_user, mocker):
        """
        Should raise a ValidationError when the incoming data is not valid
        """
        dish = Dish.objects.create(
            name="Lasagna",
            description="very great italian lasagna"
        )
        menu = Menu.objects.create(
            name="Menu 1",
            date=datetime.date.today()
        )
        menu.dishes.set([dish])

        order_mock = {
            "menu": str(menu.id),
            "dishes": [
                {
                    'name': "Lasagna",
                    'description': "very great italian lasagna"
                }
            ],
            "note": "spicy plz",
            "user": ""
        }
        mocker.patch.dict(os.environ, {'LIMIT_HOUR_TO_ORDER': '23'})
        serializer = OrderSerializer(context={'user': super_user},
                                     data=order_mock)

        mocker.spy(Order.objects, 'create')

        serializer.is_valid(raise_exception=True)
        serializer.save()

        Order.objects.create.assert_called_once()

    def test_update(self, mocker, super_user):
        """
        Should call instance.save() method and update the instance
        """

        dish = Dish.objects.create(
            name="Lasagna",
            description="very great italian lasagna"
        )
        menu = Menu.objects.create(
            name="Menu 1",
            date=datetime.date.today()
        )
        menu.dishes.set([dish])

        order_mock = {
            "menu": str(menu.id),
            "dishes": [
                {
                    'name': "Lasagna",
                    'description': "very great italian lasagna"
                }
            ],
            "note": "spicy plz",
            "user": ""
        }

        order = Order.objects.create(
            menu=menu,
            # dishes=order_mock['dishes'],
            note=order_mock['note'],
            user=super_user
        )

        order_update = {
            "menu": str(menu.id),
            "note": "NOT spicy plz",
            "dishes": [
                {
                    'name': "Lasagna",
                    'description': "very great italian lasagna"
                }
            ]
        }

        mocker.patch.dict(os.environ, {'LIMIT_HOUR_TO_ORDER': '23'})
        serializer = OrderSerializer(order, context={'user': super_user},
                                     data=order_update)

        mocker.spy(order, 'save')

        serializer.is_valid()
        serializer.save()

        order.refresh_from_db()

        order.save.assert_called_once()

        assert getattr(order, 'note') == order_update.get('note')
