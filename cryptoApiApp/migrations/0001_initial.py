# Generated by Django 4.2.3 on 2023-07-11 20:00

from django.db import migrations, models
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('currency', models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum')], max_length=3)),
                ('address', models.CharField(max_length=255)),
                ('private_key', encrypted_model_fields.fields.EncryptedCharField()),
            ],
        ),
    ]
