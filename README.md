# inquire-modeltest-sdk
SDK for the modeltest API

### Status
![Python testing](https://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Python%20testing/badge.svg)![Upload Python Package](https://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Upload%20Python%20Package/badge.svg)

## General
### About
SDK for inquire-modeltest API.

**HOLD**: The API is local hosted. Host adress may be changed in modeltestSDK/config.py 

## Contribute
These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
* Install Python version 3.6.9 or later from either https://www.python.org or https://www.anaconda.com.

### Use as Python package

Pip-install package from packagr.
```pip install modeltestSDK --extra-index-url https://api.packagr.app/EYvhW6SyL/ -U```

Then enter packagr credentials to initiate install.

### Code examples
Code examples, methods and use cases are found in [here](https://drive.google.com/drive/folders/1pxj8WBCVMjnYU2tzklr1oJY3OqhwqBes?usp=sharing).

These can either be opened in google Colab or downloaded and used with anacondas jupyter notebooks


### Clone the source code repository
At the desired location, run:

```git clone https://github.com/SevanSSP/inquire-modeltest-sdk.git```

### Setup Python environment
Create an isolated Python environment and activate it,

```console
python -m venv /path/to/new/virtual/environment

/path/to/new/virtual/environment/Scripts/activate
```

... and install the dev dependencies in [requirements.txt](requirements.txt),

```console
pip install -r requirements.txt
```

### Deployment
The application is published as a package to Sevans packagr site. To use this library in other projects use:

```
pip install modeltestSDK --extra-index-url https://api.packagr.app/EYvhW6SyL/ -U
```

Continue by logging in to the packagr server with your credentials.

### Pipeline

To perform a data import to either local or cloud hosted database you need to clone this repository.

1. Update the api-url in modeltestSDK/config.py
```
 Local-host: host = "http://127.0.0.1:8000"
 Azure: host = "https://inquire-modeltest-docker.azurewebsites.net"
```
2. Update campaign directory path in pipeline/run_pipeline.py

3. Perform data import:
```
python -m pipeline.run:pipeline.py
```


### Build and run application and database locally

Create a Postgres database (local or cloud) and note its *URI*.

Store the the database URI as environmental variable *MODELTESTDB_URI* in the relevant developer environment.

In a command/bash script or directly in terminal execute the below commands to migrate database to head state and start
the web application.

```
uvicorn app.main:app --reload
```

### Run the tests
To run all tests:

```
tests-start.sh 
```

This requires an enviorment variable *TEST_MODELTESTDB_URI* 


### File structure
<pre>
|-- .github  
|   |-- workflows  
|       |-- publish-package.yml # Github actions file to publish package of application to packagr  
|       |-- pytest.yml         # Github actions file to run pytest on pull and push to dev / master 
|
|-- scripts  
|   |-- test.sh        # Bash file to run pytest coverage  
|
|-- modeltestSDK  
|   |-- config.py # Configure connection to API
|   |-- client.py # Client handeling all HTTP-requests to API
|   |-- exceptions.py # Handles error messages from failed HTTP-requests
|   |-- api_resources.py # Abstraction layer betweem client and user-side
|   |-- resources.py # Client-side classes and functions for campaign, timeseries ... etc
|   |-- plot_timeseries # Function for plotting one or more timeseries using matplotlib
|   |-- utils.py # Utility functions used in several parts of the SDK
|
|-- pipeline
|   |-- run_pipeline.py # Script handeling pipeline of STT-campaign
|   |-- add_campaign.py
|   |-- add_sensors.py
|   |-- add_floater_test.py
|   |-- add_timeseries.py
|
|-- .gitignore
|-- Requirements.txt   # File containing all python packages used
|-- LICENSE
|-- setup.py # Setup file configuring the python package uploaded to Packagr
</pre>



### Versioning
This project uses semantic versioning. [More info](https://semver.org/)

Given a version number MAJOR.MINOR.PATCH, increment the:

* MAJOR version has incompatible API changes,
* MINOR version add functionality in a backwards compatible manner, and
* PATCH version for backwards compatible bug fixes.

**Important:** Keep the API and SDK to the same major versioning

## Authors
* **Jørgen Engelsen** - [joreng2607](https://github.com/joreng2607)
* **Nicolai Brummenæs** - [nicolai-sevan](https://github.com/nicolai-sevan)
* **Haakon Lyngstad** - [haakoly](https://github.com/haakoly)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## See also
* [modeltest API](https://github.com/SevanSSP/inquire-modeltest)
