from modeltestsdk.resources import Campaign
from pandas import DataFrame
import uuid
import datetime


def test_types(new_campaign):
    assert isinstance(new_campaign, Campaign)
    assert isinstance(uuid.UUID(new_campaign.id), uuid.UUID)
    assert isinstance(new_campaign.name, str)
    assert isinstance(new_campaign.description, str)
    assert isinstance(new_campaign.date, datetime.datetime)
    assert isinstance(new_campaign.location, str)


def test_topandas(new_campaign):
    df = new_campaign.to_pandas()
    assert isinstance(df, DataFrame)
