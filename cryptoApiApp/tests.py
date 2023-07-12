from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker
from .models import CryptoAddress


class CryptoAddressTests(APITestCase):
    def setUp(self):
        """
        Setup for the test cases.
        """
        self.fake = Faker()
        self.currency = "BTC"
        self.address = self.fake.sha256()
        self.private_key = self.fake.sha256()

        # Create a test address
        self.crypto_address = CryptoAddress.objects.create(
            currency=self.currency,
            address=self.address,
            private_key=self.private_key
        )

        # URL for our API endpoint
        self.url = reverse('crypto-address-list')

    def test_create_address(self):
        """
        Ensure we can create a new address.
        """
        data = {
            'currency': self.currency,
            'num_addresses': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CryptoAddress.objects.count(), 2)
        self.assertEqual(CryptoAddress.objects.latest('id').currency, self.currency)

    def test_create_address_invalid_currency(self):
        """
        Ensure we cannot create an address with unsupported currency.
        """
        data = {
            'currency': "UNSUPPORTED",
            'num_addresses': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_address_invalid_num_addresses(self):
        """
        Ensure we cannot create an address with num_addresses less than 1.
        """
        data = {
            'currency': self.currency,
            'num_addresses': 0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
