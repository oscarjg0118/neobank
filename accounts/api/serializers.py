from rest_framework import serializers
from accounts.models import Account, Transaction
from users.api.serializers import UserSerializer


class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["id", "user", "balance", "is_active"]
        read_only_fields = ("is_active",)

    def get_balance(self, obj):
        return obj.get_balance()


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["type", "account", "amount", "timestamp"]
        read_only_fields = ("timestamp",)
