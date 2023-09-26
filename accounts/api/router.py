from rest_framework.routers import DefaultRouter
from accounts.api.views import AccountViewSet

router_accounts = DefaultRouter()
router_accounts.register(prefix="", basename="accounts", viewset=AccountViewSet)
