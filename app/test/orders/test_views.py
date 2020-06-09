import pytest
import json
from orders.views import GenericOrderView
from orders.models import Order
from dishes.models import Dish
from menus.models import Menu
from datetime import date
from test.helper import AuthAPIRequestFactory
import os

import datetime


@pytest.mark.django_db
class TestOrderApiView:
    def test_create(self, mocker, super_user):
        """
        Should return status code 201 and return the created order
        """
        mocker.patch.dict(os.environ, {'LIMIT_HOUR_TO_ORDER': '23'})

        url = 'order/'
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
            note=order_mock['note'],
            user=super_user
        )

        request = AuthAPIRequestFactory().post(
            super_user, url, order_mock, format='json')

        mocker.patch.object(Order.objects, 'create', return_value=order)
        response = GenericOrderView.as_view()(request).render()

        content = json.loads(response.content)
        assert response.status_code == 201
        assert str(menu.id) in content['menu']
        assert order_mock['note'] in content['note']

        Order.objects.create.assert_called_once()

    def test_list(self, mocker, super_user):
        """
        Should return status code 200 and get an array with just one order
        """
        url = 'order/'
        dish = Dish.objects.create(
            name="Lasagna",
            description="very great italian lasagna"
        )
        menu = Menu.objects.create(
            name="Menu 1",
            date=datetime.date.today()
        )
        menu.dishes.set([dish])
        Order.objects.create(
            menu=menu,
            note='not spicy plz',
            user=super_user
        )

        request = AuthAPIRequestFactory().get(
            super_user, url, format='json')

        response = GenericOrderView.as_view()(request).render()

        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == 1

    def test_retrieve(self, mocker, super_user):
        """
        Should return status code 200 and get the specific order
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
        order = Order.objects.create(
            menu=menu,
            note='not spicy plz',
            user=super_user
        )
        id = str(order.id)
        url = "order/{0}/".format(id)

        request = AuthAPIRequestFactory().get(super_user, url, format='json')

        response = GenericOrderView.as_view()(request, id=id).render()

        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('id') == str(order.id)
