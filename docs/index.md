# Welcome to the documentation Inquire Model Test Python SDK

## About
A Python software developer kit (SDK) for the Inquire Model Test API by Sevan, version 2.

## Getting started
Pip-install the package from Sevan's package index:
```console
pip install modeltestsdk --extra-index-url https://api.repoforge.io/EYvhW6SyL/
```

### Sign in
The SDK signs in with Microsoft. Set these environment variables (or pass them to `Config`):

- INQUIRE_MODELTEST_API_HOST: the API, e.g. https://inquire-modeltest.azurewebsites.net
- INQUIRE_MODELTEST_TENANT_ID: Sevan's Microsoft tenant
- INQUIRE_MODELTEST_API_CLIENT_ID: the model test API's app registration
- INQUIRE_MODELTEST_CLIENT_ID: the app you sign in with (a public client for users)

The first `Client()` opens the browser for sign-in; the token is kept in a cache on disk, so later sessions don't
ask again. A service principal also sets INQUIRE_MODELTEST_CLIENT_SECRET. A web app can give the client a `token`,
a `token_provider` or an azure-identity `credential` instead.

What you can read follows your access in the API: read access per campaign, given through groups; writing needs
write access to the campaign, creating campaigns the Admin role.

### Prerequisites
* Python 3.10 or later
