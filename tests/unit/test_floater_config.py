import pytest
from modeltestSDK.resources import FloaterConfiguration, FloaterConfigurations
from uuid import uuid4

def test_floater_configuration(new_floater_configuration):
    assert isinstance(new_floater_configuration, FloaterConfiguration)
    assert isinstance(new_floater_configuration.name, str)
    assert isinstance(new_floater_configuration.description, str)
    assert isinstance(new_floater_configuration.characteristic_length, float)


def test_floater_configurations(new_floater_configuration, new_sensor, new_campaign):
    floaterconfigs = FloaterConfigurations([new_floater_configuration])

    assert len(floaterconfigs) == 1
    assert len(floaterconfigs.to_pandas()) == 1

    with pytest.raises(TypeError):
        failed_floaterconfigs = FloaterConfigurations([new_floater_configuration, new_sensor])

    with pytest.raises(TypeError):
        floaterconfigs.append(new_sensor)

    fc2 = FloaterConfiguration(
        name="test2",
        description="description",
        campaign_id=new_campaign.id,
        characteristic_length=2.0,
        draft=1.0,
    )
    fc2.id = str(uuid4())
    floaterconfigs.append(fc2)

    assert len(floaterconfigs) == 2

    fc_check = floaterconfigs.get_by_id(fc2.id)
    assert fc_check == fc2

    with pytest.raises(KeyError):
        floaterconfigs.get_by_id('notfoundid')