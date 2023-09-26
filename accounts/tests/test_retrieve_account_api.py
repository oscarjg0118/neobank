from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Account
from users.models import User


class RetrieveAccountAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="adminuser",
            password="testpass",
            email="adminuser@test.com",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="regularuser",
            password="testpass",
            email="regularuser@test.com",
            is_staff=False,
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpass",
            email="otheruser@test.com",
            is_staff=False,
        )
        self.account = Account.objects.create(user=self.regular_user)
        self.url = f"/api/accounts/{self.account.id}/"

    def test_admin_can_view_any_account(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_view_own_account(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_view_other_users_account(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_view_account(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_404_for_nonexistent_account(self):
        self.client.force_authenticate(user=self.admin_user)
        nonexistent_account_url = "/api/accounts/999999/"

        response = self.client.get(nonexistent_account_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
