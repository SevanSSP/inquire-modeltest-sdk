import pytest
from modeltestsdk.resources import FloaterConfig, FloaterConfigs
from uuid import uuid4

def test_floater_configuration(new_floater_configuration):
    assert isinstance(new_floater_configuration, FloaterConfig)
    assert isinstance(new_floater_configuration.name, str)
    assert isinstance(new_floater_configuration.description, str)
    assert isinstance(new_floater_configuration.characteristic_length, float)


def test_floater_configurations(new_floater_configuration, new_sensor, new_campaign):
    floater_configs = FloaterConfigs([new_floater_configuration])

    assert len(floater_configs) == 1
    assert len(floater_configs.to_pandas()) == 1

    with pytest.raises(TypeError):
        failed_floater_configs = FloaterConfigs([new_floater_configuration, new_sensor])

    with pytest.raises(TypeError):
        floater_configs.append(new_sensor)

    fc2 = FloaterConfig(
        name="test2",
        description="description",
        campaign_id=new_campaign.id,
        characteristic_length=2.0,
        draft=1.0,
    )
    fc2.id = str(uuid4())
    floater_configs.append(fc2)

    assert len(floater_configs) == 2

    fc_check = floater_configs.get_by_id(fc2.id)
    assert fc_check == fc2

    assert floater_configs.get_by_id('notfoundid') is None
