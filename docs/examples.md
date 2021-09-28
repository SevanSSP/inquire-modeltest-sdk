#Examples

## Basic

Initiate API client and fetch all available campaigns.


```python hl_lines="7-8"
--8<--- "basic.py"
```

!!! note

    the get_all() method was previously used to return several results

##Create campaign

Add a campaign to the database, using datetime to properly handle the date.

```python hl_lines="8-14"
--8<--- "create.py"
```

##Get campaign
This example will filter by campaign name and description and sort ascending by date.
The filter object enables use of Pythonic syntax 


```python hl_lines="7-10"
--8<--- "filter_and_sort.py"
```

!!! note

    Filtering and sort arguments needs to be contained inside a list.
    Sorting will be done in the order the arguments are given in the list

!!! note

    the get_all() method was previously used to return several results



 


