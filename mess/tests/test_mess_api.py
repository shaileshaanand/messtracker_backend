import pytest
from django.urls import reverse
from rest_framework import status
from faker import Faker
from mess.serializers import MessSerializer

faker = Faker()

MESS_URL = reverse("mess:mess-list")


def mess_url(mess_external_id):
    return reverse("mess:mess-detail", args=[mess_external_id])


@pytest.mark.django_db
class TestMessPublicAPI:
    def test_list_fails(self, create_mess, rest_client):
        mess = create_mess()
        resp = rest_client.get(MESS_URL)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_fails(self, create_mess, rest_client):
        mess = create_mess()
        resp = rest_client.get(mess_url(mess.external_id))
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_fails(self, create_mess, rest_client, create_user):
        # mess = create_mess()
        payload = {"name": faker.name(), "owner": create_user().external_id}
        resp = rest_client.post(MESS_URL, payload, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestMessPrivateAPI:
    def test_list_fails_normal_user(self, authenticated_rest_client, create_mess):
        client, user = authenticated_rest_client
        create_mess()
        resp = client.get(MESS_URL)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_get_fails_normal_user(self, authenticated_rest_client, create_mess):
        client, user = authenticated_rest_client
        mess = create_mess()
        resp = client.get(mess_url(mess.external_id))
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_create_fails_normal_user(self, create_mess, authenticated_rest_client):
        # mess = create_mess()
        client, user = authenticated_rest_client
        payload = {"name": faker.name(), "owner": user.external_id}
        resp = client.post(MESS_URL, payload, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_list(self, superuser_authenticated_rest_client, create_mess):
        client, _ = superuser_authenticated_rest_client
        mess1 = create_mess()
        mess2 = create_mess()
        resp = client.get(MESS_URL)
        assert resp.status_code == status.HTTP_200_OK
        assert MessSerializer(mess1).data in resp.data
        assert MessSerializer(mess2).data in resp.data

    def test_get(self, superuser_authenticated_rest_client, create_mess):
        client, _ = superuser_authenticated_rest_client
        mess = create_mess()
        resp = client.get(mess_url(mess.external_id))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == MessSerializer(mess).data

    def test_update(self, superuser_authenticated_rest_client, create_mess):
        client, _ = superuser_authenticated_rest_client
        mess = create_mess()
        new_name = faker.name()
        resp = client.patch(
            mess_url(mess.external_id), payload={"name": new_name}, format="json"
        )
        mess.refresh_from_db()
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == MessSerializer(mess).data

    def test_create(self, superuser_authenticated_rest_client, create_mess):
        client, super_user = superuser_authenticated_rest_client

        payload = {"name": faker.name(), "owner": super_user.external_id}
        resp = client.post(MESS_URL, payload=payload, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
