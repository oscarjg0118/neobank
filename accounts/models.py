from django.db import models
from django.db.models import Sum, Case, When, F
from django.utils.translation import gettext_lazy as _
from users.models import User
from accounts.enums import TransactionType


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def get_balance(self):
        transactions = Transaction.objects.filter(account=self.id)

        # Calcula el saldo sumando los depósitos y restando los retiros
        balance = transactions.annotate(
            adjusted_amount=Case(
                When(type=TransactionType.DEPOSIT, then=F("amount")),
                When(type=TransactionType.WITHDRAW, then=F("amount") * -1),
                default=0,
                output_field=models.DecimalField(),
            )
        ).aggregate(balance=Sum("adjusted_amount"))["balance"]
        if balance is None:
            return 0
        return balance

    class Meta:
        verbose_name = _("bank account")
        verbose_name_plural = _("bank accounts")


class Transaction(models.Model):
    type = models.IntegerField(
        choices=[(tag.value, tag.name) for tag in TransactionType],
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{_(self.get_type_display())} - {self.amount} - {self.timestamp}"
