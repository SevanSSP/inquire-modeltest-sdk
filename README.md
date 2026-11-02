# inquire-modeltest-sdk

## About
Python software developer kit (SDK) for the Sevan model test API (version 2: Microsoft sign-in, datapoints in Azure
Blob as Parquet, statistics computed by the API).

## Status
![Pytest with minimum 95% coverage](https://github.com/SevanSSP/inquire-modeltest-sdk/actions/workflows/test.yml/badge.svg?branch=master)![Security check - Bandit](https://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Security%20check%20-%20Bandit/badge.svg?branch=master)![Build documentation](https://github.com/SevanSSP/inquire-modeltest-sdk/workflows/Build%20documentation/badge.svg?branch=master)

## Get started
Install the SDK from Sevan's private package index:

```
pip install modeltestsdk --extra-index-url https://api.repoforge.io/EYvhW6SyL/
```

Sign in with your Microsoft account (the browser opens the first time; the token is kept in a cache on disk):

```python
from modeltestsdk import Client

with Client() as client:  # settings from INQUIRE_MODELTEST_* environment variables, see .env-template
    campaign = client.campaign.get_by_name("Bream FPSO").scalar()
    ts = campaign.tests()[0].timeseries()[0]
    data = ts.get_data()                 # the default window; all_data=True for the whole record
    stats = ts.get_statistics()          # stored statistics over the default window
    window = ts.get_statistics(start=2000, end=4000)   # computed on request over a custom window
```

A service principal (e.g. the import pipeline) signs in with `INQUIRE_MODELTEST_CLIENT_SECRET` as well; a web app can
pass `token=`, `token_provider=` or an azure-identity `credential=` to `Client`. Visit the
[documentation](https://sevanssp.github.io/inquire-modeltest-sdk/) for more.

## What changed in 4.0
- Microsoft (Entra) sign-in instead of user name and password; no administrator or secret keys. Creating campaigns
  needs the Admin role in the API; everything else follows your read or write access per campaign.
- Datapoints are no longer posted: the import pipeline uploads one Parquet file per test and time base
  (`client.test.upload_datafile`, `modeltestsdk.datafile.write_datafile`), and the API computes the statistics.
  `Timeseries.add_data` and `TimeseriesAPI.add_data_points` are gone.
- Upserts on natural keys for the pipeline (`client.campaign.upsert`, `upsert_many` on floater configs, sensors,
  tests, timeseries and tags) and import runs (`client.import_runs`).
- The v2 fields on the resources: the campaign's coordinate definitions and main hull diameter, the floater config's
  heading, VCG and hull geometry, the sensor's z reference and measured axis, the timeseries' points and time range.
- New: statistics over a custom window, `FloaterConfig.coordinates()`, `Campaign.documents()` and
  `download_document()`.

## Contribute

### Set up the Python environment
Install Python 3.10 or later and [uv](https://docs.astral.sh/uv/). At the project root, run

```console
uv sync --group dev
```

### Testing
The unit tests run against an in-memory stand-in for the API:

```console
uv run pytest tests
```

or `nox -s tests` (with the 95 % coverage check, as in CI). The functional tests only read, and run against a real
API when it is given, signed in from the INQUIRE_MODELTEST_* settings:

```console
uv run pytest tests/functional --api=https://inquire-modeltest-staging.azurewebsites.net
```

## Versioning
This project uses semantic versioning. [More info](https://semver.org/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors
* **Jørgen Engelsen** - [joreng2607](https://github.com/joreng2607)
* **Per Voie** - [tovop](https://github.com/tovop)
* **Snorre Fjellvang** - [snorrefjellvang](https://github.com/snorrefjellvang)
* **Einar Glomnes** - [EBGlom](https://github.com/EBGlom)
