from django.contrib.auth import get_user_model
from rest_framework import serializers

from ledger.models import Account, Transaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "phone_number", "is_active", "is_admin"]


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "account_number",
            "balance",
            "initial_balance",
            "created_at",
            "updated_at",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True, many=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "transaction_type",
            "date",
            "created_at",
        ]