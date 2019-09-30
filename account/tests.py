from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from account.models import Account


class AccountTests(APITestCase):
    def setUp(self):
        """
        Ensure we can create an administrator user and we can authenticate with him
        """
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = 'Token ' + Token.objects.create(user=self.user).key

    def test_create_account(self):
            """
            Ensure we can create a new account object.
            """
            self.client.force_login(user=self.user)
            url = reverse('accounts:accounts_add')
            data = {
                'first_name': 'Agustin',
                'last_name': 'Martinez',
                'iban': 'ES7620770024003102575766'
            }
            response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=self.token)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Account.objects.count(), 1)
            self.assertEqual(Account.objects.get().iban, 'ES7620770024003102575766')


    def get_all_accounts(self):
        """
        Ensure we can retrieve all accounts data
        """
        self.client.force_login(user=self.user)
        url = reverse('accounts:accounts')
        response = self.client.get(url, {}, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 1)

    def update_account(self):
        """
        Ensure we can update account data
        """
        self.client.force_login(user=self.user)
        url = reverse('accounts:accounts_modify')
        data = {
            'id': Account.objects.get(iban='ES7620770024003102575766'),
            'first_name': 'Eva',
            'last_name': 'Perez',
            'iban': 'ES7620770024003102575766'
        }
        response = self.client.put(url, data, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().first_name, 'Eva')

    def delete_account(self):
        """
        Ensure we can delete the account we created
        """
        self.client.force_login(user=self.user)
        url = reverse('accounts:accounts_delete')
        data = {
            'id': Account.objects.get(iban='ES7620770024003102575766'),
            'first_name': 'Eva',
            'last_name': 'Perez',
            'iban': 'ES7620770024003102575766'
        }
        response = self.client.delete(url, data, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 0)
