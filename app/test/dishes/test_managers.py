import pytest
from rest_framework.exceptions import ValidationError, NotFound
from dishes.models import Dish
from datetime import date
from uuid import uuid4


@pytest.mark.django_db
class TestDishManager:
    @pytest.mark.parametrize('dishes', [
        ([{'name': 'Lasagna',
            'description': 'Italian Dish'},
          {'name': 'Sushi',
            'description': 'Japaneese Dish'}]),
    ])
    def test_validate_dishes(self, dishes):
        """
        Should return Dishes the 2 dishes that are already created
        """
        for dish in dishes:
            Dish.objects.create(**dish)
        validate_dishes = Dish.objects.validate_dishes(dishes)

        assert len(validate_dishes) == len(dishes)

    @pytest.mark.parametrize('dishes', [
        ([{'name': 'Lasagna',
            'description': 'Italian Dish'}]),
    ])
    def test_not_validate_dishes(self, dishes):
        """
        Should raise a ValidationError when one of the dishes does not exist in the database
        """

        with pytest.raises(NotFound):
            Dish.objects.validate_dishes(dishes)
