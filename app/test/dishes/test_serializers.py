import pytest
from rest_framework.exceptions import ValidationError
from dishes.serializers import DishSerializer


@pytest.mark.django_db
class TestDishSerializer:
    @pytest.mark.parametrize('dish', [
        ({'name': 'Lasagna',
            'description': 'Italian Dish'}),
    ])
    def test_valid_incoming_data(self, dish):
        """
        Should return True when the data is valid
        """

        serializer = DishSerializer(data=dish)

        assert serializer.is_valid()

    @pytest.mark.parametrize('dish', [
        ([{'name': 'Lasagna',
            'description': 25}]),
    ])
    def test_invalid_data(self, dish):
        """
        Should raise a ValidationError when the data is not valid
        """

        serializer = DishSerializer(data=dish)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
