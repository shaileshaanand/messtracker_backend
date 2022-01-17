from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework import status

from faker import Faker
import pytest

from core.models import User

user_model: User = get_user_model()
faker = Faker()

CREATE_USER_URL = reverse("user:create")
CREATE_TOKEN_URL = reverse("user:token")
USER_URL = reverse("user:me")


@pytest.mark.django_db
class TestPublicUserApi:
    def test_create_valid_user_success(self, rest_client):
        payload = {
            "email": faker.email(),
            "password": faker.password(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
        }

        res = rest_client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED
        user = user_model.objects.get(external_id=res.data["external_id"])
        assert user.check_password(payload["password"])
        assert "password" not in res.data
        assert "external_id" in res.data
        assert res.data["first_name"] == payload["first_name"]
        assert res.data["last_name"] == payload["last_name"]

    def test_user_exists(self, rest_client, create_user):
        """Text creating user with email that already exists"""
        payload = {
            "email": faker.email(),
            "password": faker.password(),
        }
        create_user(**payload)
        res = rest_client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
