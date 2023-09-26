from decimal import Decimal
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from accounts.api.serializers import AccountSerializer, TransactionSerializer
from accounts.models import Account, Transaction
from accounts.api.permissions import IsAdminUserOrIsOwnerUser, IsOwnerUser


class AccountViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsAdminUserOrIsOwnerUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class TransactionViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated, IsOwnerUser]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(account=self.kwargs["account_pk"])

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["account"] = self.kwargs["account_pk"]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        account = Account.objects.get(id=data["account"])
        self.check_object_permissions(self.request, account)
        balance = account.get_balance()
        if data["type"] == 2 and balance - Decimal(data["amount"]) < 0:
            return Response(
                data={"message": "Insufficient funds"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
