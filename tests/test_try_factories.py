import tests.factories
import pytest


@pytest.mark.django_db
def test_fac():
    mi1 = tests.factories.MealItemFactory.create()
    mi2 = tests.factories.MealItemFactory.create()
    mi3 = tests.factories.MealItemFactory.create()
    mi4 = tests.factories.MealItemFactory.create()
    # print(tests.factories.MessFactory.create())
    # print(tests.factories.UserFactory.create())

    print(tests.factories.MealFactory.create())
    # print(tests.factories.MealItemFactory.create())

    print(tests.factories.MenuFactory.create())
