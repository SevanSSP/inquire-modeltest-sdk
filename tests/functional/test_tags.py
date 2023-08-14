from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool


def test_tag_api(client, secret_key, new_tags):
    """The Api is now verified good to go and tests can interact with it"""
    tagged_sensor_ids, tagged_test_ids, tagged_timeseries_ids = [], [], []

    for tag in new_tags:
        client.tag.get_by_id(tag.id)
        client.tag.get_by_name(tag.name)

        if tag.sensor_id:
            get_tags = client.tag.get_by_sensor_id(tag.sensor_id)
            for get_tag in get_tags:
                assert get_tag in new_tags
                tagged_sensor_ids.append(get_tag.sensor_id)
        elif tag.test_id:
            get_tags = client.tag.get_by_test_id(tag.test_id)
            for get_tag in get_tags:
                assert get_tag in new_tags
                tagged_test_ids.append(get_tag.test_id)
        elif tag.timeseries_id:
            get_tags = client.tag.get_by_timeseries_id(tag.timeseries_id)
            for get_tag in get_tags:
                assert get_tag in new_tags
                if get_tag.timeseries_id:
                    tagged_timeseries_ids.append(get_tag.timeseries_id)
        else:
            # orphan tag
            tag.delete(secret_key=secret_key)

    tags = []
    for sensor_id in set(tagged_sensor_ids):
        tags.extend(client.tag.get(filter_by=[client.filter.tag.sensor_id == sensor_id]))
    for test_id in set(tagged_test_ids):
        tags.extend(client.tag.get(filter_by=[client.filter.tag.test_id == test_id]))
    for timeseries_id in set(tagged_timeseries_ids):
        tags.extend(client.tag.get(filter_by=[client.filter.tag.timeseries_id == timeseries_id]))

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


def test_tag_limit_skip(client, new_tags):
    all_tags = client.tag.get(limit=10000)

    portion = max(1, len(all_tags) // 5)
    part_of_tags = client.tag.get(limit=portion, skip=0)
    assert len(part_of_tags) == portion

    n_skips = -(len(all_tags) // -portion)  # ceiling divide

    all_tags_in_steps = []
    for skip in range(n_skips):
        all_tags_in_steps.extend(client.tag.get(limit=portion, skip=skip * portion))

    assert len(all_tags_in_steps) == len(all_tags)
    for tag in all_tags:
        assert tag in all_tags_in_steps
