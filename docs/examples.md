#Examples

## Basic

Initiate API client and fetch all available campaings.

!!! note

    Line numbers are shown by default and `examples` is configured as base path for the snippets. These
    settings are controlled in the `mkdocs.yaml`.
    
    Snippets shall therefore be put in the `examples` folder on the root and referenced using the filename only.
    
    `hl_lines="7-8"` hihglights lines 7 and 8 in the code snippet.
    
    
!!! warning

    An error is raised if the referenced file is not found.    


```python hl_lines="7-8"
--8<--- "basic.py"
```

##Create campaign

``` python linenums="1"
from datetime import datetime
from modeltestSDK import Client

client = Client()

campaign = client.campaign.create(name="Campaign name",
                                  description="Campaign description",
                                  date=datetime(year=2000, month=1, day=1).isoformat(),
                                  location="Test location",
                                  scale_factor=52,
                                  water_depth=300,
                                  read_only=True) 
```

Import datetime to properly handle the date
``` python linenums="1" hl_lines="1"
from datetime import datetime
from modeltestSDK import Client

```

Import and initialize the client
``` python linenums="2" hl_lines="1 3"
from modeltestSDK import Client

client = Client()
```

Add necessary inputs
``` python linenums="5" hl_lines="1-8"
campaign = client.campaign.create(name="Campaign name",
                                  description="Campaign description",
                                  date=datetime(year=2000, month=1, day=1).isoformat(),
                                  location="Test location",
                                  scale_factor=52,
                                  water_depth=300,
                                  read_only=True) 
```