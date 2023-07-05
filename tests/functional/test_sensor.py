from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool
import random

def test_sensor_api(client, secret_key, admin_key, new_campaigns):
    """The Api is now verified good to go and tests can interact with it"""
    campaign = new_campaigns[0]
    campaign_id=campaign.id
    name=random_lower_string()
    description=random_lower_string()
    unit=random_lower_short_string()
    kind=random.choice([
        "length",
        "velocity",
        "acceleration",
        "force",
        "pressure",
        "volume",
        "mass",
        "moment",
        "angle",
        "angular velocity",
        "angular acceleration",
        "slamming force",
        "slamming pressure",
        "control signal",
        "rate"])
    source=random.choice([
        "direct measurement",
        "basin derived",
        "Sevan derived",
        "external derived"])
    x=random_float()
    y=random_float()
    z=random_float()
    position_reference=random.choice([
        "local",
        "global"])
    position_draft_lock=random_bool()
    position_heading_lock=random_bool()
    positive_direction_definition=random_lower_string()
    area=random_float()

    sensor = client.sensor.create(name=name,description=description,unit=unit,kind=kind,source=source,x=x,y=y,z=z,
                                  position_reference=position_reference,position_heading_lock=position_heading_lock,position_draft_lock=position_draft_lock,
                                  positive_direction_definition=positive_direction_definition,campaign_id=campaign_id, area=area)
    assert client.sensor.get_by_name(name)

    sensors = client.sensor.get(filter_by=[
        client.filter.sensor.name == name,
        client.filter.sensor.description == description],
        sort_by=[client.sort.sensor.kind.asc])

    assert len(sensors) == 1
    assert sensors[0] == client.sensor.get_by_name(name) == client.sensor.get_by_id(sensors[0].id)
    assert client.sensor.get_by_name('not existing name') is None
    assert len(client.sensor.get()) == 1

    sensor_with_same_name = client.sensor.create(name=name,description='description',unit=unit,kind=kind,source=source,x=x,y=y,z=z,
                                  position_reference=position_reference,position_heading_lock=position_heading_lock,position_draft_lock=position_draft_lock,
                                  positive_direction_definition=positive_direction_definition,campaign_id=campaign_id, area=area)
    assert sensor_with_same_name.id != sensor.id
    assert client.sensor.get_by_name(name) == client.sensor.get_by_id(sensor.id)
    assert client.sensor.get_by_name(name) != client.sensor.get_by_id(sensor_with_same_name.id)

    client.sensor.delete(sensor.id, secret_key=secret_key)
    client.sensor.delete(sensor_with_same_name.id, secret_key=secret_key)

