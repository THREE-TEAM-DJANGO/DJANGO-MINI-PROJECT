from django.contrib.auth import get_user_model
from rest_framework import serializers

from ledger.models import Account, Transaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "phone_number", "is_active", "is_admin"]


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Account
        fields = [
            "user",
            "account_number",
            "balance",
            "initial_balance",
            "created_at",
            "updated_at",
        ]
    def create(self, validated_data):
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError("User 정보가 없습니다")
        return Account.objects.create(user=user, **validated_data)

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True, many=False)

    class Meta:
        model = Transaction
        fields = [
            "account",
            "amount",
            "bank_code",
            "analysis_type",
            "transaction_type",
            "date",
            "created_at",
        ]