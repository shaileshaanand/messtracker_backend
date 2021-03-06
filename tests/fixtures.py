from rest_framework.test import APIClient
import pytest

from core.models import MealItem, User, Meal, Menu, Mess
from .factories import (
    MealFactory,
    UserFactory,
    MealItemFactory,
    MessFactory,
    MenuFactory,
    SuperUserFactory,
)


@pytest.fixture(scope="function")
def create_user():
    def _create_user(**kwargs) -> User:
        return UserFactory.create(**kwargs)

    return _create_user


@pytest.fixture(scope="function")
def create_superuser():
    def _create_superuser(**kwargs) -> User:
        return SuperUserFactory.create(**kwargs)

    return _create_superuser


@pytest.fixture(scope="function")
def rest_client():
    return APIClient()


@pytest.fixture(scope="function")
def authenticated_rest_client(create_user):
    user = create_user()
    client = APIClient()
    client.force_authenticate(user)
    return (client, user)


@pytest.fixture(scope="function")
def superuser_authenticated_rest_client(create_superuser):
    user = create_superuser()
    client = APIClient()
    client.force_authenticate(user)
    return (client, user)


@pytest.fixture(scope="function")
def create_meal_item():
    def _create_meal_item(**kwargs) -> MealItem:
        return MealItemFactory.create(**kwargs)

    return _create_meal_item


@pytest.fixture(scope="function")
def create_meal():
    def _create_meal(**kwargs) -> Meal:
        return MealFactory.create(**kwargs)

    return _create_meal


@pytest.fixture(scope="function")
def create_mess():
    def _create_mess(**kwargs) -> Mess:
        return MessFactory.create(**kwargs)

    return _create_mess


@pytest.fixture(scope="function")
def create_menu():
    def _create_menu(**kwargs) -> Menu:
        return MenuFactory.create(**kwargs)

    return _create_menu
