from modeltestSDK.resources import Sensor
from pandas import DataFrame
import datetime
import uuid


def test_types(new_sensor):
    assert isinstance(new_sensor, Sensor)
    #assert isinstance(new_sensor.id, uuid.UUID)
    assert isinstance(new_sensor.name, str)
    assert isinstance(new_sensor.description, str)
    assert isinstance(new_sensor.unit, str)
    assert isinstance(new_sensor.kind, str)
    assert isinstance(new_sensor.x, float)
    assert isinstance(new_sensor.y, float)
    assert isinstance(new_sensor.z, float)
    assert isinstance(new_sensor.is_local, bool)
    assert isinstance(new_sensor.campaign_id, str)

def test_topandas(new_sensor):
    df = new_sensor.to_pandas()
    assert isinstance(df, DataFrame)