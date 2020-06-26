import pytest
from datetime import datetime
from modeltestSDK import Campaign

@pytest.fixture(scope="module")
def new_campaign():
    camp = Campaign(
        name = "asdfg",
        description = "sdh dfgh rghh",
        date = datetime.utcnow(),
        location= "Ålesund",
        diameter= 2.2,
        scale_factor= 1,
        water_density= 1024,
        water_depth= 1200,
        transient= 1
        )
    return camp