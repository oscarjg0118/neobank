from django.urls import path
from accounts.api.views import AccountView

urlpatterns = [
    path("", AccountView.as_view(), name="account"),
]
