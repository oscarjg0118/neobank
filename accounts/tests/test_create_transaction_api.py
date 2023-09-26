from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Account
from users.models import User
from accounts.enums import TransactionType


class CreateTransactionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", email="testuser@test.com"
        )
        self.account = Account.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.url = f"/api/accounts/{self.account.id}/transactions/"

        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass", email="otheruser@test.com"
        )
        self.other_account = Account.objects.create(user=self.other_user)
        self.other_account_url = f"/api/accounts/{self.other_account.id}/transactions/"

    def test_create_transaction(self):
        for transaction_type in [TransactionType.DEPOSIT, TransactionType.WITHDRAW]:
            with self.subTest(transaction_type=transaction_type):
                data = {
                    "type": transaction_type,
                    "amount": "5000.00",
                }
                response = self.client.post(self.url, data, format="json")
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data["account"], self.account.id)
                self.assertEqual(response.data["type"], transaction_type)
                self.assertEqual(response.data["amount"], str(data["amount"]))
                self.assertIn("timestamp", response.data)

    def test_account_balance_after_transaction(self):
        initial_balance = self.account.get_balance()

        # Test Deposit Transaction
        deposit_amount = Decimal("500.00")
        deposit_data = {"type": TransactionType.DEPOSIT, "amount": deposit_amount}
        deposit_response = self.client.post(self.url, deposit_data, format="json")
        self.assertEqual(deposit_response.status_code, status.HTTP_201_CREATED)

        # Refresh account instance to get updated balance
        self.account.refresh_from_db()
        self.assertEqual(self.account.get_balance(), initial_balance + deposit_amount)

        # Test Withdraw Transaction
        withdraw_amount = Decimal("200.00")
        withdraw_data = {"type": TransactionType.WITHDRAW, "amount": withdraw_amount}
        withdraw_response = self.client.post(self.url, withdraw_data, format="json")
        self.assertEqual(withdraw_response.status_code, status.HTTP_201_CREATED)

        # Refresh account instance to get updated balance
        self.account.refresh_from_db()
        self.assertEqual(
            self.account.get_balance(),
            initial_balance + deposit_amount - withdraw_amount,
        )

    def test_authentication_required(self):
        # Logout user to perform unauthenticated request
        self.client.logout()

        # Try to create a deposit transaction without authentication
        deposit_data = {"type": TransactionType.DEPOSIT, "amount": "500.00"}
        deposit_response = self.client.post(self.url, deposit_data, format="json")
        self.assertEqual(deposit_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to create a withdrawal transaction without authentication
        withdraw_data = {"type": TransactionType.WITHDRAW, "amount": "200.00"}
        withdraw_response = self.client.post(self.url, withdraw_data, format="json")
        self.assertEqual(withdraw_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_required(self):
        # Intentar crear una transacción de depósito en la cuenta de otro usuario
        deposit_data = {"type": TransactionType.DEPOSIT, "amount": "500.00"}
        deposit_response = self.client.post(
            self.other_account_url, deposit_data, format="json"
        )
        self.assertEqual(deposit_response.status_code, status.HTTP_403_FORBIDDEN)

        # Intentar crear una transacción de retiro en la cuenta de otro usuario
        withdraw_data = {"type": TransactionType.WITHDRAW, "amount": "200.00"}
        withdraw_response = self.client.post(
            self.other_account_url, withdraw_data, format="json"
        )
        self.assertEqual(withdraw_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_insufficient_balance(self):
        # Establecer el saldo inicial de la cuenta a un valor específico mediante transacciones válidas
        initial_balance = Decimal("100.00")
        deposit_data = {"type": TransactionType.DEPOSIT, "amount": initial_balance}
        deposit_response = self.client.post(self.url, deposit_data, format="json")
        self.assertEqual(deposit_response.status_code, status.HTTP_201_CREATED)

        # Intentar crear una transacción de retiro con un monto mayor que el saldo disponible
        withdraw_amount = Decimal("200.00")
        withdraw_data = {"type": TransactionType.WITHDRAW, "amount": withdraw_amount}
        withdraw_response = self.client.post(self.url, withdraw_data, format="json")

        # Comprobar que el código de estado de la respuesta es 400 Bad Request, indicando que la transacción no está permitida
        self.assertEqual(withdraw_response.status_code, status.HTTP_400_BAD_REQUEST)

        # Refrescar la instancia de la cuenta y comprobar que el saldo no ha cambiado
        self.account.refresh_from_db()
        self.assertEqual(self.account.get_balance(), initial_balance)

    def test_list_transactions(self):
        # Crear varias transacciones para la cuenta
        transaction_count = 5
        for _ in range(transaction_count):
            deposit_data = {"type": TransactionType.DEPOSIT, "amount": "100.00"}
            deposit_response = self.client.post(self.url, deposit_data, format="json")
            self.assertEqual(deposit_response.status_code, status.HTTP_201_CREATED)

        # Realizar una solicitud GET para listar las transacciones de la cuenta
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar que el número de transacciones listadas es correcto
        self.assertEqual(len(response.data), transaction_count)

        # Verificar los detalles de cada transacción listada
        for transaction_data in response.data:
            self.assertIn("type", transaction_data)
            self.assertIn("amount", transaction_data)
            self.assertIn("timestamp", transaction_data)
            self.assertEqual(transaction_data["account"], self.account.id)
