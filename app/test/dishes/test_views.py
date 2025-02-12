import pytest
import json
from dishes.views import DishAPIView
from dishes.models import Dish
from test.helper import AuthAPIRequestFactory


@pytest.mark.django_db
class TestDishApiView:
    def test_create(self, mocker, super_user):
        """
        Should call dish.objects.create and return status code 201
        """
        url = 'dish/'
        dish = {
            'name': 'Lasagna',
            'description': 'Italian Dish'
        }
        request = AuthAPIRequestFactory().post(
            super_user, url, dish, format='json')

        mocker.patch.object(Dish.objects, 'create', return_value=dish)
        response = DishAPIView.as_view()(request).render()

        content = json.loads(response.content)

        assert response.status_code == 201
        assert 'Lasagna' in content['name']

        Dish.objects.create.assert_called_once()

    def test_list(self, mocker, super_user):
        """
        Should return status code 200 and return on dish 
        """
        Dish.objects.create(
            name='Lasagna',
            description='Italian Dish'
        )
        url = 'dish/'

        request = AuthAPIRequestFactory().get(
            super_user, url, format='json')

        response = DishAPIView.as_view()(request).render()

        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == 1

    def test_update(self, mocker, super_user):
        """
        Should return status code 200 and retrieve the updated dish
        """
        dish = Dish.objects.create(
            name='Lasagna',
            description='Italian Dish'
        )
        id = str(dish.id)
        dish_edited = {
            'name': 'Lasagna edited',
            'description': 'Italian Dish Edited'
        }

        url = "dish/{0}/".format(id)

        request = AuthAPIRequestFactory().put(
            super_user, url, dish_edited, format='json')

        response = DishAPIView.as_view()(request, id=id).render()

        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('id') == str(dish.id)
        assert content.get('name') == dish_edited.get('name')

    def test_retrieve(self, mocker, super_user):
        """
        Should return status code 200 and return the specific dish
        """
        dish = Dish.objects.create(
            name='Lasagna',
            description='Italian Dish'
        )
        id = str(dish.id)
        url = "dish/{0}/".format(id)

        request = AuthAPIRequestFactory().get(super_user, url, format='json')

        response = DishAPIView.as_view()(request, id=id).render()

        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('id') == str(dish.id)

    def test_delete(self, mocker, super_user):
        """
        Should return status code 204
        """
        dish = Dish.objects.create(
            name='Lasagna',
            description='Italian Dish'
        )
        id = str(dish.id)

        url = "dish/{0}/".format(id)
        request = AuthAPIRequestFactory().delete(super_user, url, format='json')

        response = DishAPIView.as_view()(request, id=id).render()

        assert response.status_code == 204
