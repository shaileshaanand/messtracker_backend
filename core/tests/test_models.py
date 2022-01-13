import pytest
from django.contrib.auth import get_user_model

user_model = get_user_model()
User = user_model


@pytest.mark.django_db
class TestUser:
    def test_create_user_with_email_successful(self):
        """Test Creating a new user with an email is successful"""
        email = "test@test.com"
        password = "test@1234"
        first_name = "test"
        last_name = "user"
        user = user_model.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.check_password(password) is True
        assert user.role == "student"

    def test_new_user_invalid_email(self):
        with pytest.raises(ValueError):
            get_user_model().objects.create_user(None, "123")

    def test_create_new_superuser(self):
        user: User = get_user_model().objects.create_superuser(
            "test@test.com", "123", first_name="admin", last_name="user"
        )
        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.role == "owner"

    def test_create_staff_with_email_successful(self):
        """Test Creating a new user with an email is successful"""
        email = "test@test.com"
        password = "test@1234"
        first_name = "test"
        last_name = "user"
        user = user_model.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
        )
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.check_password(password) is True
        assert user.role == "staff"

    def test_user_last_modified_date(self):
        password = "test@1234"
        email = "test@tESt.com"
        first_name = "test"
        last_name = "user"
        user: User = user_model.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.save()
        assert user.last_modified_date is not None
        modified_date = user.last_modified_date
        user.first_name = "test2"
        user.save()
        assert user.last_modified_date > modified_date

    def test_user_name_string(self):
        password = "test@1234"
        email = "test@tESt.com"
        first_name = "test"
        last_name = "user"
        user: User = user_model.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.save()
        assert user.name() == first_name + " " + last_name
