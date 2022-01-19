import pytest


from faker import Faker

from core.models import User

fake = Faker()


@pytest.mark.django_db
class TestUser:
    def test_create_user_with_email_successful(self, create_user):
        """Test Creating a new user with an email is successful"""
        email = fake.email()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        user: User = create_user(
            email=email, password=password, first_name=first_name, last_name=last_name
        )
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.created_at is not None
        assert user.check_password(password)
        assert user.role == "student"

    def test_create_user_email_normalized(self, create_user):
        """Test Creating a new user with an email is successful"""
        email = "test@tESt.com"
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        user: User = create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        assert user.email == email.lower()
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.check_password(password)

    def test_new_user_invalid_email(self, create_user):
        with pytest.raises(ValueError):
            create_user(email=None)

    def test_create_new_superuser(self, create_user):
        user: User = create_user(is_superuser=True, is_staff=True)
        assert user.is_superuser
        assert user.is_staff

    def test_user_last_modified_date(self, create_user):
        user: User = create_user()
        assert user.last_modified_date is not None
        prev_modified_date = user.last_modified_date
        user.first_name = fake.first_name()
        user.save()
        assert user.last_modified_date > prev_modified_date

    def test_user_name_string(self, create_user):
        user: User = create_user()
        user.save()
        assert user.name() == user.first_name + " " + user.last_name


# @pytest.mark.db
# class TestMealItem:

#     def create_meal_item_success(self):
