from rest_framework.test import APIClient
import pytest

from core.models import MealItem, User
from .factories import UserFactory, MealItemFactory


@pytest.fixture(scope="function")
def create_user():
    def _create_user(**kwargs) -> User:
        return UserFactory.create(**kwargs)

    return _create_user


@pytest.fixture(scope="function")
def rest_client():
    return APIClient()


@pytest.fixture(scope="function")
def create_meal_item():
    def _create_meal_item(**kwargs) -> MealItem:
        return MealItemFactory.create(**kwargs)

    return _create_meal_item

# @pytest.fixture(scope="function")
