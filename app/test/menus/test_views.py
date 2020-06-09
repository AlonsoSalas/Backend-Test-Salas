import pytest
import json
from menus.views import GenericMenuAPIView
from menus.models import Menu
from datetime import date
from test.helper import AuthAPIRequestFactory


@pytest.mark.django_db
class TestMenuApiView:
    def test_create(self, mocker, super_user):
        """
        Should return status code 201 and return the created menu
        """
        url = 'menu/'
        menu = {
            'name': 'Lasagna',
            'date': '2020-01-01',
            'dishes': []
        }
        request = AuthAPIRequestFactory().post(
            super_user, url, menu, format='json')

        mocker.patch.object(Menu.objects, 'create', return_value=menu)
        response = GenericMenuAPIView.as_view()(request).render()

        content = json.loads(response.content)

        assert response.status_code == 201
        assert 'Lasagna' in content['name']

        Menu.objects.create.assert_called_once()

    def test_list(self, mocker, super_user):
        """
        Should return status code 200 return an array of 1 menu
        """
        Menu.objects.create(
            name='Lasagna',
            date='2020-01-01'
        )
        url = 'menu/'

        request = AuthAPIRequestFactory().get(
            super_user, url, format='json')

        response = GenericMenuAPIView.as_view()(request).render()

        content = json.loads(response.content)
        assert response.status_code == 200
        assert len(content) == 1

    def test_update(self, mocker, super_user):
        """
        Should return status code 200 and retrieve the updated menu
        """
        menu = Menu.objects.create(
            name='Lasagna',
            date='2020-01-01'
        )
        id = str(menu.id)
        menu_edited = {
            'name': 'Lasagna edited',
            'date': '2020-01-01',
            'dishes': []
        }

        url = "menu/{0}/".format(id)

        request = AuthAPIRequestFactory().put(
            super_user, url, menu_edited, format='json')

        response = GenericMenuAPIView.as_view()(request, id=id).render()

        content = json.loads(response.content)
        assert response.status_code == 200
        assert content.get('id') == str(menu.id)
        assert content.get('name') == menu_edited.get('name')

    def test_retrieve(self, mocker, super_user):
        """
        Should return status code 200 and return the specific menu
        """
        menu = Menu.objects.create(
            name='Lasagna',
            date='2020-01-01'
        )
        id = str(menu.id)
        url = "menu/{0}/".format(id)

        request = AuthAPIRequestFactory().get(super_user, url, format='json')

        response = GenericMenuAPIView.as_view()(request, id=id).render()

        content = json.loads(response.content)

        assert response.status_code == 200
        assert content.get('id') == str(menu.id)

    def test_delete(self, mocker, super_user):
        """
        Should return status code 204
        """
        menu = Menu.objects.create(
            name='Lasagna',
            date='2020-01-01'
        )
        id = str(menu.id)

        url = "menu/{0}/".format(id)
        request = AuthAPIRequestFactory().delete(super_user, url, format='json')

        response = GenericMenuAPIView.as_view()(request, id=id).render()

        assert response.status_code == 204
