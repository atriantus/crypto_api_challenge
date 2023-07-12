# Crypto Address Generator API

This is a simple REST API for generating cryptocurrency addresses. It currently supports generating addresses for Bitcoin, Ethereum, Dogecoin, Litecoin, and TRON.

## Setup

1. Clone this repository.
2. Navigate to the repository's root directory.
3. Run `pip install -r requirements.txt` to install the required dependencies.
4. Run `python manage.py makemigrations` followed by `python manage.py migrate` to set up the database.

## Running the Project

1. Start the Django server by running `python manage.py runserver`.
2. The API endpoints will now be accessible at `http://localhost:8000`.

## API Endpoints

The API provides the following endpoints:

- `POST /addresses/`: Generate a new cryptocurrency address.
  - Request body should include `currency` (the type of cryptocurrency, e.g., 'BTC' for Bitcoin) and `num_addresses` (the number of addresses to generate, optional, defaults to 1).
  - Returns the created addresses and private keys.
- `GET /addresses/`: List all previously generated addresses.
- `GET /addresses/{id}/`: Retrieve a previously generated address by its ID.

## Manually Testing the Project

You can test the API endpoints manually using a tool such as curl or Postman. Here are some example curl commands:

- Generate a new Bitcoin address: `curl -X POST http://localhost:8000/addresses/ -d "currency=BTC"`
- Generate 5 Ethereum addresses: `curl -X POST http://localhost:8000/addresses/ -d "currency=ETH&num_addresses=5"`
- List all addresses: `curl -X GET http://localhost:8000/addresses/`
- Retrieve address with ID 1: `curl -X GET http://localhost:8000/addresses/1/`

## Running the Tests

This project includes tests for the main functionality. To run the tests, use the command `python manage.py test`.

## Adding Support for More Cryptocurrencies

To add support for a new cryptocurrency, you will need to:
1. Add a new choice for the `currency` field in the `CryptoAddress` model.
2. Update the `create` method in `CryptoAddressViewSet` to handle the new currency.

Make sure that the library you are using for address and key generation supports the cryptocurrency you want to add.
