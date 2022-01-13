from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

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
