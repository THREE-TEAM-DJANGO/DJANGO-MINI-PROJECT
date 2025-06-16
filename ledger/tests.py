from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ledger.models import Account, Transaction

# Create your tests here.

User = get_user_model()


class AccountListViewTest(APITestCase):
    def setUp(self):
        # 테스트 유저 생성
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.url = reverse("account_list")

        Account.objects.create(user=self.user, account_number="Test Account 1", balance=0)
        Account.objects.create(user=self.user, account_number="Test Account 2", balance=0,)

    def test_authenticated_user_can_get_account_list(self):
        # 로그인 처리
        self.client.login(username="testuser", password="testpw123")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_unauthenticated_user_cannot_access_account_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountCreateViesTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="<testpw123>"
        )

        self.client = APIClient()
        self.clien.force_authenticate(user=self.user)
        self.url = reverse("account_create")


    def test_create_account_success(self):
        data = {
            "account_number": "123"
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "계좌가 생성되었습니다")
        self.assertEqual(response.data["account_number"], "123")
        self.assertTrue(Account.objects.filter(account_number="123").exists())


    def test_create_account_missing_fields(self):
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("account_number", response.data)


    def test_create_account_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {"account_number": "0012"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpw123")
        self.other_user = User.objects.create_user(username="otheruser", password="testpw456")

        self.account = Account.objects.create(
            user=self.user,
            account_number="12345"
        )
        self.client = APIClient()
        self.url = reverse("account-delete", args=[self.account.pk])

    def test_delete_own_account_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(pk=self.account.pk).exists())

    def test_delete_other_user_account_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TransactionCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpw123")
        self.other_user = User.objects.create_user(username="otheruser", password="testpw456")

        self.user_account = Account.objects.create(
            user=self.user,
            account_number="111"
        )

        self.other_account = Account.objects.create(
            user=self.other_user,
            account_number="999"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("transaction-create")

    def test_create_transaction_success(self):
        data = {
            "account": self.user_account.pk,
            "type": "DEPOSIT",
            "amount": 10000
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 10000)
        self.assertEqual(response.data["type"], "DEPOSIT")

    def test_create_transaction_invalid_data(self):
        data = {
            "account": self.user_account.pk,
            "type": "",  # 잘못된 타입
            "amount": -1000  # 음수 금액
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TransactionListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpw123")
        self.other_user = User.objects.create_user(username="otheruser", password="testpw456")

        self.account1 = Account.objects.create(user=self.user, account_number="111122223333")
        self.account2 = Account.objects.create(user=self.user, account_number="222233334444")
        self.other_account = Account.objects.create(user=self.other_user, account_number="999988887777")

        # 거래 데이터 생성
        Transaction.objects.create(account=self.account1, type="DEPOSIT", amount=10000)
        Transaction.objects.create(account=self.account1, type="WITHDRAWAL", amount=5000)
        Transaction.objects.create(account=self.account2, type="DEPOSIT", amount=20000)
        Transaction.objects.create(account=self.other_account, type="DEPOSIT", amount=30000)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("transaction-list")


class TransactionUpdateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpw123")

        self.account = Account.objects.create(
            user=self.user,
            account_number="12345"
        )

        self.transaction = Transaction.objects.create(
            account=self.account,
            type="DEPOSIT",
            amount=10000
        )

        self.client = APIClient()
        self.url = reverse("transaction-update", args=[self.transaction.pk])


    def test_update_transaction_success(self):
        data = {
            "type": "WITHDRAWAL",
            "amount": 20000
        }
        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "WITHDRAWAL")
        self.assertEqual(response.data["amount"], 20000)


class TransactionDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpw123")

        self.account = Account.objects.create(
            user=self.user,
            account_number="123456"
        )

        self.transaction = Transaction.objects.create(
            account=self.account,
            type="DEPOSIT",
            amount=10000
        )

        self.client = APIClient()
        self.url = reverse("transaction-delete", args=[self.transaction.pk])

    def test_delete_transaction_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(pk=self.transaction.pk).exists())