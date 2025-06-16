from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from ledger.constants import ANALYSIS_TYPES, BANK_CODES, TRANSACTION_TYPE
from member.models import User

# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    bank_code = models.CharField(max_length=10, unique=True, choices=BANK_CODES)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    analysis_type = models.CharField(max_length=10, choices=ANALYSIS_TYPES)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.transaction_type}"
