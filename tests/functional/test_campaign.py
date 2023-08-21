from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool


def test_campaign_api(client, secret_key, admin_key):
    """The Api is now verified good to go and tests can interact with it"""
    name = random_lower_string()
    description = random_lower_string()
    date = str(datetime.now())
    location = random_lower_string()
    scale_factor = random_float()
    water_depth = random_float()
    camp = client.campaign.create(name, description, location, date, scale_factor, water_depth, admin_key)
    assert client.campaign.get_by_name(name)

    campaigns = client.campaign.get(filter_by=[
        client.filter.campaign.name == name,
        client.filter.campaign.description == description],
        sort_by=[client.sort.campaign.date.asc])

    assert len(campaigns) == 1
    assert campaigns[0] == client.campaign.get_by_id(campaigns[0].id)
    assert campaigns[0] in client.campaign.get_by_name(name)
    assert len(client.campaign.get_by_name('not existing name')) == 0

    camp_with_same_name = client.campaign.create(name, 'description', 'location', date, scale_factor, water_depth,
                                                 admin_key)
    assert camp_with_same_name.id != camp.id
    assert client.campaign.get_by_id(camp.id) in client.campaign.get_by_name(name)
    assert client.campaign.get_by_id(camp_with_same_name.id) in client.campaign.get_by_name(name)

    client.campaign.delete(camp.id, secret_key=secret_key)
    client.campaign.delete(camp_with_same_name.id, secret_key=secret_key)


def test_campaign_resources(client, new_campaigns, new_sensors, new_tests, new_floaterconfig):
    campaigns_from_db = client.campaign.get(limit=999999)

    for campaign in new_campaigns:
        assert campaign in campaigns_from_db

        sensors_from_db = client.sensor.get(filter_by=[client.filter.sensor.campaign_id == campaign.id])

        for sensor in campaign.sensors():
            assert sensor in sensors_from_db
            assert sensor in new_sensors

        for sensor in sensors_from_db:
            assert sensor in campaign.sensors()
            assert sensor in new_sensors

        fc_from_db = client.floaterconfig.get(filter_by=[client.filter.floaterconfig.campaign_id == campaign.id])

        for fc in campaign.floater_configurations():
            assert fc in fc_from_db

        tests_from_db = client.test.get(filter_by=[client.filter.test.campaign_id == campaign.id])
        for test in campaign.tests():
            assert test in tests_from_db

    camp_name = new_campaigns[0].name
    camp_list = new_campaigns
    camp_list_filtered = camp_list.filter(name=camp_name)
    assert len(camp_list_filtered) == 1
    camp_list.filter(name=camp_name, inplace=True)
    assert len(camp_list) == 1



def test_update_campaign(client, new_campaigns, secret_key):
    for campaign in new_campaigns:
        campaign.name = campaign.name + 'new'
        campaign.update(secret_key=secret_key)

        assert campaign in client.campaign.get_by_name(campaign.name)


def test_campaign_resource(client, new_campaigns, new_tests):
    camp = new_campaigns[0]
    for test in camp.tests().filter(type='Floater Test'):
        assert test in new_tests


def test_campaign_limit_skip(client, new_campaigns):
    all_campaigns = client.campaign.get(limit=10000)

    portion = max(1, len(all_campaigns) // 5)
    if len(all_campaigns) % portion != 0:
        portion += 1
    part_of_campaigns = client.campaign.get(limit=portion, skip=0)
    assert len(part_of_campaigns) == portion

    n_skips = -(len(all_campaigns) // -portion)  # ceiling divide

    all_campaigns_in_steps = []
    for skip in range(n_skips):
        all_campaigns_in_steps.extend(client.campaign.get(limit=portion, skip=skip * portion))

    assert len(all_campaigns_in_steps) == len(all_campaigns)
    for campaign in all_campaigns:
        assert campaign in all_campaigns_in_steps
