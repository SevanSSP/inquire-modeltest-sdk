from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool


def test_tag_api(client, secret_key, new_tags):
    """The Api is now verified good to go and tests can interact with it"""
    for i, tag in enumerate(new_tags):
        print(f'{i} / {len(new_tags)}')
        client.tag.get_by_id(tag.id)
        assert len(client.tag.get_by_name(tag.name)) > 0
        if tag.sensor_id:
            client.tag.get_by_sensor_id(tag.sensor_id)
        elif tag.test_id:
            client.tag.get_by_test_id(tag.test_id)
        else:
            client.tag.get_by_timeseries_id(tag.timeseries_id)

    tags = client.tag.get()
    for tag in tags:
        assert tag in new_tags
        assert client.tag.get_by_id(tag.id) == tag
        if tag.sensor_id:
            tag_test = client.tag.get_by_sensor_id(tag.sensor_id)
        elif tag.test_id:
            tag_test = client.tag.get_by_test_id(tag.test_id)
        else:
            tag_test = client.tag.get_by_timeseries_id(tag.timeseries_id)
        assert tag in tag_test

