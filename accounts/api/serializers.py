from rest_framework import serializers
from accounts.models import Account
from users.api.serializers import UserSerializer


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Account
        fields = ["id", "user", "balance", "is_active"]
        read_only_fields = ("balance", "is_active")
