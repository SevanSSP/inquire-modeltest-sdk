# inquire-modeltest-sdk

## About
Python software developer kit (SDK) for the Sevan modeltest API

## Status
![Pytest with minimum 95% coverage](https://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Build%20and%20test%20package/badge.svghttps://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Pytest%20with%20minimum%2095%%20coverage/badge.svg?branch=master)![Build documentation](https://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Build%20documentation/badge.svg?branch=master)![Publish Python package to Packagr](https://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Publish%20Python%20package%20to%20Packagr/badge.svg?branch=master)

## Get started
Install the SDK from Sevan's private package index by

```
pip install modeltestSDK --extra-index-url https://api.packagr.app/EYvhW6SyL/
```

Visit the [documentation](https://sevanssp.github.io/inquire-modeltest-sdk/) to learn how to use it.

## Contribute
These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Install Python version 3.9.1 or later from either https://www.python.org or https://www.anaconda.com.

We use Poetry for dependency management and packaging. Install it as shown [here](https://python-poetry.org/docs/#installation).

### Clone the source code repository
At the desired location, run:

```git clone https://github.com/SevanSSP/inquire-modeltest-sdk.git```

### Set up the Python environment
At the project root, run

```console
poetry install
```

... to create a virtual environement and install the dependencies.

Now you are ready to code!

### Testing
To run all tests

```console
pytest tests
```

or

```console
nox
```

Local testing requires that the model test API is running at http://127.0.0.1:8000 (local host)


## Versioning
This project uses semantic versioning. [More info](https://semver.org/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors
* **Jørgen Engelsen** - [joreng2607](https://github.com/joreng2607)
* **Per Voie** - [tovop](https://github.com/tovop)
* **Snorre Fjellvang** - [tovop](https://github.com/snorrefjellvang)
* **Einar Glomnes** - [EBGlom](https://github.com/EBGlom)


