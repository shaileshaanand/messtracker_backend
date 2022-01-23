from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError("Users must have email address")

        user = self.model(email=self.normalize_email(email), *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(email, password, *args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseModel(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now=True)
    last_edited_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=512, unique=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        self.last_modified_date = timezone.now()
        super(User, self).save(*args, **kwargs)

    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def role(self):
        if self.is_superuser:
            return "owner"
        if self.is_staff:
            return "staff"
        return "student"


class Mess(BaseModel):

    name = models.CharField(max_length=255, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}, Owner: {self.owner.name()}"


class MealItem(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self) -> str:
        return f"MealItem: {self.name}"


class Meal(BaseModel):
    class MEAL_TYPE(models.TextChoices):
        BREAKFAST = "BR", _("BREAKFAST")
        LUNCH = "LU", _("LUNCH")
        SNACKS = "SN", _("SNACKS")
        DINNER = "DI", _("DINNER")

    name = models.CharField(max_length=255, null=False, blank=False)
    current_price = models.IntegerField()
    type = models.CharField(
        max_length=2, choices=MEAL_TYPE.choices, null=False, blank=False
    )
    meal_items = models.ManyToManyField(MealItem)

    def __str__(self):
        # items = ",".join([f"{item.name}" for item in self.meal_items.all()])
        return f"name {self.name} price {self.current_price} type {self.type}"


class Menu(BaseModel):

    breakfast_meal = models.ForeignKey(
        Meal, on_delete=models.PROTECT, related_name="breakfast_meal"
    )
    lunch_meal = models.ForeignKey(
        Meal, on_delete=models.PROTECT, related_name="lunch_meal"
    )
    snacks_meal = models.ForeignKey(
        Meal, on_delete=models.PROTECT, related_name="snacks_meal"
    )
    dinner_meal = models.ForeignKey(
        Meal, on_delete=models.PROTECT, related_name="dinner_meal"
    )
    date = models.DateField()
    mess = models.ForeignKey(Mess, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"Menu -> breakfast:f{self.breakfast_meal}\nlunch:f{self.lunch_meal}\nsnacks:f{self.snacks_meal}\ndinner:f{self.dinner_meal}"
