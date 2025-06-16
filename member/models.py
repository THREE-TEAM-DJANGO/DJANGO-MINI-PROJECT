from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("사용자명은 필수입니다")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('관리자는 is_admin=True 이어야 합니다.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField(max_length=30, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
