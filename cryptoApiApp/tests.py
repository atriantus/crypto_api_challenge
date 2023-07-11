from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CryptoAddress
from .serializers import CryptoAddressSerializer


class CryptoAddressTests(APITestCase):
    def test_generate_address(self):
        # Test the "Generate Address" endpoint
        url = reverse('crypto-address-list')
        data = {'currency': 'BTC'}

        # Send a POST request to the endpoint
        response = self.client.post(url, data, format='json')

        # Assert that the response has a status code of 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the generated address and private key from the response
        address = response.data['address']
        private_key = response.data['private_key']

        # Validate the generated address and private key using your chosen method

    def test_list_addresses(self):
        # Test the "List Address" endpoint
        url = reverse('crypto-address-list')

        # Create some CryptoAddress instances for testing
        CryptoAddress.objects.create(currency='BTC', address='BTC1...', private_key='...')
        CryptoAddress.objects.create(currency='ETH', address='ETH1...', private_key='...')

        # Send a GET request to the endpoint
        response = self.client.get(url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get all CryptoAddress instances from the database
        addresses = CryptoAddress.objects.all()

        # Serialize the addresses using the serializer
        serializer = CryptoAddressSerializer(addresses, many=True)

        # Assert that the returned data matches the serialized data
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_address(self):
        # Test the "Retrieve Address" endpoint
        address = CryptoAddress.objects.create(currency='BTC', address='BTC1...', private_key='...')
        url = reverse('crypto-address-detail', kwargs={'pk': address.pk})

        # Send a GET request to the endpoint
        response = self.client.get(url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Serialize the address
        serializer = CryptoAddressSerializer(address)

        # Assert that the returned data matches the serialized data
        self.assertEqual(response.data, serializer.data)