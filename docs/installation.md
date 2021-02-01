# Installation
## Use as Python package

Pip-install package from packagr.
```console
pip install modeltestSDK --extra-index-url https://api.packagr.app/EYvhW6SyL/ -U
```

## Set up environmental variables

- INQUIRE_MODELTEST_API_USER
- INQUIRE_MODELTEST_API_PASSWORD
- INQUIRE_MODELTEST_API_HOST

Where

- USER is you Inquire Model Test DB username, e.g "user"
- PASSWORD is your password, e.g "pass", and 
- HOST is the API host, e.g "http://127.0.0.1:8000", when hosting locally


## Contribute
These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
* Install Python 3, version 3.6.9 or later

### Clone the source code repository
At the desired location, run:

```git clone https://github.com/SevanSSP/inquire-modeltest-sdk.git```

### Setup Python environment
Poetry


### Run the tests
To run all tests:

```console
pytest tests 
```