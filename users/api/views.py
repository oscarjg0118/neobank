from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.api.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from users.models import User
from users.api.permissions import IsAdminUserOrIsOwnerUser


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOrIsOwnerUser]

    def get(self, request, user_id=None):
        user = get_object_or_404(User, id=user_id) if user_id else request.user
        self.check_object_permissions(self.request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        self.check_object_permissions(self.request, user)
        serializer = UserUpdateSerializer(user, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
