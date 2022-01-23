import random
import factory

from django.contrib.auth import get_user_model
from core.models import Meal, MealItem, Menu, Mess, User as UserModel

User: UserModel = get_user_model()

MEAL_ITEMS = [
    "roti",
    "daal",
    "chawal",
    "puri",
    "paratha",
    "idli",
    "sambhar",
    "vada",
    "chutney",
    "papad",
    "salad",
    "mix veg",
    "chola",
    "bhatura",
    "paneer",
    "chicken",
]

MEALS = [
    "Puri Sabji",
    "Idli",
    "Chicken",
    "Kofta",
    "Rajma Chawal",
    "Chicken Chiili",
    "Mix Veg",
]

MESS_NAMES = ["hostel no.20", "hostel no.21"]


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


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_superuser(*args, **kwargs)


class MessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mess

    owner = factory.SubFactory(UserFactory)
    name = factory.Faker("numerify", text="Mess ##")


class MealItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MealItem

    name = factory.LazyFunction(lambda: random.choice(MEAL_ITEMS))


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meal

    name = factory.LazyFunction(lambda: random.choice(MEALS))
    current_price = factory.Faker("random_int", min=40, max=100, step=5)
    type = factory.LazyFunction(
        lambda: random.choice([x.value for x in Meal.MEAL_TYPE])
    )

    @factory.post_generation
    def meal_items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for meal_item in extracted:
                self.meal_items.add(meal_item)
        else:
            for _ in range(random.randint(2, 6)):
                self.meal_items.add(MealItemFactory())


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    breakfast_meal = factory.SubFactory(MealFactory)
    lunch_meal = factory.SubFactory(MealFactory)
    snacks_meal = factory.SubFactory(MealFactory)
    dinner_meal = factory.SubFactory(MealFactory)
    date = factory.Faker("date")
    mess = factory.SubFactory(MessFactory)
