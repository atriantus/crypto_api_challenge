from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import bitcoinlib.wallets as bw
from eth_account import Account
from .models import CryptoAddress
from .serializers import CryptoAddressSerializer

# from hdwallet import HDWallet
# from hdwallet.utils import generate_entropy
# from hdwallet.symbols import DOGE as SYMBOL


# ViewSet for handling the API endpoints
class CryptoAddressViewSet(viewsets.ModelViewSet):

    # Define the queryset and the serializer
    queryset = CryptoAddress.objects.all()
    serializer_class = CryptoAddressSerializer


    # Overriding the create() method for custom address generation
    def create(self, request, *args, **kwargs):
        # Fetch the 'currency' from request data
        currency = request.data.get('currency')

        # Function for generating a Bitcoin address
        def generate_btc_address():
            # Create a new Wallet or open the existing one if same name
            w = bw.wallet_create_or_open('test_wallet')
            # Get an address from the wallet
            address = w.get_key().address
            # Get the private key from the wallet
            private_key = w.get_key().wif
            return address, private_key

        # Function for generating an Ethereum address
        def generate_eth_address():
            # Create a new Ethereum account
            account = Account.create()
            # Get the address of the account
            address = account.address
            # Get the private key of the account
            private_key_hex = account.key
            private_key = private_key_hex.hex()
            return address, private_key

        # Mapping the currencies to their respective address generation functions
        address_generators = {
            'BTC': generate_btc_address,
            'ETH': generate_eth_address,
        }

        # Check if the currency is supported
        if currency not in address_generators:
            return Response({'error': 'Unsupported currency'}, status=400)

        # Generate the address and the private key
        address, private_key = address_generators[currency]()

        # Create a new CryptoAddress instance and save it to the database
        crypto_address = CryptoAddress.objects.create(
            currency=currency,
            address=address,
            private_key=private_key
        )

        # Serialize the created CryptoAddress instance
        serializer = self.get_serializer(crypto_address)
        return Response(serializer.data, status=201) # Return the serialized data
