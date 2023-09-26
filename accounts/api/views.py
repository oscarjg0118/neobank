from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from accounts.api.serializers import AccountSerializer
from accounts.models import Account
from accounts.api.permissions import IsAdminUserOrIsOwnerUser


class AccountViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsAdminUserOrIsOwnerUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
