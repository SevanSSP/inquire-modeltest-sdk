# Examples

## Basic

Initiate API client and fetch all available campaigns.

```python hl_lines="7-8"
--8<--- "basic.py"
```

## Create campaign

Add a campaign to the database, using datetime to properly handle the date. Creating a campaign needs the Admin
role; the import pipeline uses `client.campaign.upsert` instead.

```python hl_lines="8-14"
--8<--- "create.py"
```

## Get campaign
This example will filter by campaign name and description and sort ascending by date.
The filter object enables use of Pythonic syntax

```python hl_lines="7-10"
--8<--- "filter_and_sort.py"
```

!!! note

    Filtering and sort arguments needs to be contained inside a list.
    Sorting will be done in the order the arguments are given in the list

## Data and statistics
A timeseries' data over its default window or all of it, and its statistics: stored over the default window, or
computed on request over a custom window.

```python
--8<--- "data_and_statistics.py"
```

## Documents
A campaign's reports and drawings, listed and downloaded.

```python
--8<--- "documents.py"
```
