from rest_framework import serializers
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "user", "balance", "is_active"]
