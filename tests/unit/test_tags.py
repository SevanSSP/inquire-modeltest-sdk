from modeltestsdk.resources import Tag
import uuid


def test_types(new_tags):
    for tag in new_tags:
        assert isinstance(tag, Tag)
        assert isinstance(uuid.UUID(tag.id), uuid.UUID)
        assert isinstance(tag.name, str)
        assert isinstance(tag.comment, str)
        if tag.test_id:
            assert isinstance(uuid.UUID(tag.test_id), uuid.UUID)
        if tag.sensor_id:
            assert isinstance(uuid.UUID(tag.sensor_id), uuid.UUID)
        if tag.timeseries_id:
            assert isinstance(uuid.UUID(tag.timeseries_id), uuid.UUID)


def test_references(new_tags):
    for tag in new_tags:
        assert tag.sensor is None
        assert tag.test is None
        assert tag.timeseries is None
