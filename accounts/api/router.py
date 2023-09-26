from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from accounts.api.views import AccountViewSet, TransactionViewSet

router_accounts = SimpleRouter()
router_accounts.register("", AccountViewSet)

transactions_router = NestedSimpleRouter(router_accounts, "", lookup="account")
transactions_router.register(
    "transactions", TransactionViewSet, basename="account-transactions"
)
