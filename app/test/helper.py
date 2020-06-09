import pytest

from rest_framework.test import force_authenticate, APIRequestFactory


class AuthAPIRequestFactory(APIRequestFactory):
    def get(self, user, *args, **kwargs):
        request = super().get(*args, **kwargs)
        force_authenticate(request, user=user)
        return request

    def post(self, user, *args, **kwargs):
        request = super().post(*args, **kwargs)
        force_authenticate(request, user=user)
        return request

    def put(self, user, *args, **kwargs):

        request = super().put(*args, **kwargs)
        force_authenticate(request, user=user)
        return request

    def delete(self, user, *args, **kwargs):
        request = super().delete(*args, **kwargs)
        force_authenticate(request, user=user)
        return request


@ pytest.fixture
def regular_user(db, django_user_model):
    return django_user_model.objects.create_user(
        email='regular@gmail.com', password="regular", username="regular")


@pytest.fixture
def super_user(db, django_user_model):
    return django_user_model.objects.create_superuser(
        email='admin@gmail.com', password="1234", username="admin")
