from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class AccountAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@test.com",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("account")

    def test_create_account(self):
        data = {"user": self.user.id}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIsInstance(response.data["id"], int)
        self.assertIsNotNone(response.data["user"])
        self.assertEqual(response.data["balance"], "0.00")
        self.assertTrue(response.data["is_active"])

    def test_user_can_have_only_one_account(self):
        # Crear la primera cuenta
        data = {"user": self.user.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Intentar crear una segunda cuenta para el mismo usuario
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_unauthenticated(self):
        # Desautenticar al cliente
        self.client.logout()

        # Intentar crear una cuenta sin estar autenticado
        data = {"user": self.user.id}
        response = self.client.post(self.url, data, format="json")

        # Verificar que la respuesta tiene un estado 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_account_non_admin(self):
        # Crear un usuario no administrador y autenticarse con él
        non_admin_user = User.objects.create_user(
            username="nonadmin",
            password="testpass",
            email="nonadmin@test.com",
            is_staff=False,
        )
        self.client.force_authenticate(user=non_admin_user)

        # Intentar crear una cuenta siendo un usuario no administrador
        data = {"user": non_admin_user.id}
        response = self.client.post(self.url, data, format="json")

        # Verificar que la respuesta tiene un estado 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
