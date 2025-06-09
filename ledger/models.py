from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.



class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ("INCOME", "입금"),
        ("EXPENSE", "출금"),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.transaction_type}"