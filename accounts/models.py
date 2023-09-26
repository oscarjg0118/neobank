from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("bank account")
        verbose_name_plural = _("bank accounts")
