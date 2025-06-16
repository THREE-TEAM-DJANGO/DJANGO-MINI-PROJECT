from django.contrib.auth import get_user_model
from rest_framework import serializers

from ledger.models import Account, Transaction
from member.serializer import UserListSerializer

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True, many=False)

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
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError("User 정보가 없습니다")
        return Account.objects.create(user=user, **validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

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
