# Import Django models and CryptoAddress for encryption
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField



class CryptoAddress(models.Model):
    BTC = 'BTC'
    ETH = 'ETH'

    CURRENCY_CHOICES = [
        (BTC, 'Bitcoin'),
        (ETH, 'Ethereum'),
    ]

    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    address = models.CharField(max_length=255)
    private_key = EncryptedCharField(max_length=255)

    def __str__(self):
        return self.address
