import pytest
from rest_framework.exceptions import ValidationError, NotFound
from dishes.models import Dish
from datetime import date
# from ..helpers import get_future_day
from uuid import uuid4


@pytest.mark.django_db
class TestDishManager:
    @pytest.mark.parametrize('dishes', [
        ([{'name': 'Lasagna',
            'description': 'Italian Dish'},
          {'name': 'Sushi',
            'description': 'Japaneese Dish'}]),
    ])
    def test_validateDishes(self, dishes):
        """
        Should return Dishes the 2 dishes that are already created
        """
        for dish in dishes:
            Dish.objects.create(**dish)
        validateDishes = Dish.objects.validateDishes(dishes)

        assert len(validateDishes) == len(dishes)

    @pytest.mark.parametrize('dishes', [
        ([{'name': 'Lasagna',
            'description': 'Italian Dish'}]),
    ])
    def test_not_validateDishes(self, dishes):
        """
        Should raise a ValidationError when one of the dishes does not exist in the database
        """

        with pytest.raises(NotFound):
            Dish.objects.validateDishes(dishes)
