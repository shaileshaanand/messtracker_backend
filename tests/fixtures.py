import pytest

from core.models import User
from .factories import UserFactory


@pytest.fixture(scope="function")
def create_user():
    def _create_user(**kwargs) -> User:
        return UserFactory.create(**kwargs)

    return _create_user
