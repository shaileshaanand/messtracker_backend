import factory

from django.contrib.auth import get_user_model
from core.models import User as UserModel

User: UserModel = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel

    email = factory.Faker("email")
    password = factory.Faker("password")
    # TODO: add factory.django.Password after next release of factory_boy
    # password = factory.django.Password()
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_superuser = False
    is_staff = False
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)
