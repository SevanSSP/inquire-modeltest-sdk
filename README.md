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
pip install modeltestSDK -i https://api.packagr.app/EYvhW6SyL/
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


### Versioning


## Authors
* **Jørgen Engelsen** - [joreng2607](https://github.com/joreng2607)
* **Nicolai Brummenæs** - [nicolai-sevan](https://github.com/nicolai-sevan)
* **Haakon Lyngstad** - [haakoly](https://github.com/haakoly)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## See also
* [modeltest API](https://github.com/SevanSSP/inquire-modeltest)
