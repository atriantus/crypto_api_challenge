from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from hdwallet import BIP44HDWallet
from hdwallet.utils import generate_mnemonic
from .models import CryptoAddress
from .serializers import CryptoAddressSerializer

# Define constants for coin types for clarity and easy changes in future
COIN_TYPES = {
    "BTC": 0,
    "ETH": 60,
    "DOGE": 3,
    "LTC": 2,
    "TRX": 195
    # Can add all the coins hdwallet supports found at: https://hdwallet.readthedocs.io/en/v2.2.1/cryptocurrencies.html
}


class CryptoAddressViewSet(viewsets.ModelViewSet):
    queryset = CryptoAddress.objects.all()
    serializer_class = CryptoAddressSerializer

    def create(self, request, *args, **kwargs):
        currency = request.data.get('currency')
        num_addresses = int(request.data.get('num_addresses', 1))

        if not self._is_valid_request(currency, num_addresses):
            return Response({'error': 'Unsupported currency or invalid number of addresses'}, status=400)

        addresses = self._generate_addresses(currency, num_addresses)
        serializer = self.get_serializer(addresses, many=True)
        return Response(serializer.data, status=201)

    def _is_valid_request(self, currency, num_addresses):
        """
        Checks if the request is valid. i.e., currency is supported and num_addresses is >=1.
        """
        return currency in COIN_TYPES and num_addresses >= 1

    def _generate_addresses(self, currency, num_addresses):
        """
        Generates the requested number of addresses for the specified currency.
        """
        coin_type = COIN_TYPES[currency]
        mnemonic = generate_mnemonic(language="english")
        wallet = BIP44HDWallet(symbol=currency)
        wallet.from_mnemonic(mnemonic=mnemonic)
        addresses = []
        for i in range(num_addresses):
            wallet.clean_derivation()
            wallet.from_path(path=f"m/44'/{coin_type}'/0'/0/{i}")
            addresses.append(
                CryptoAddress.objects.create(
                    currency=currency,
                    address=wallet.address(),
                    private_key=wallet.private_key()
                )
            )
        return addresses