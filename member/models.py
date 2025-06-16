from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):

        if not username:
            raise ValueError("사용자명은 필수입니다")

        user = self.model(
            username=username,
            password=password,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):

        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    # password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    nickname = models.CharField(max_length=30, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
