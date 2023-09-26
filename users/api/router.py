from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.api.views import RegisterView, UserView

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", UserView.as_view()),
    path("user/<int:user_id>/", UserView.as_view(), name="user-detail-with-id"),
]
