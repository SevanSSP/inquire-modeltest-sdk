from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool, \
    random_int
import random


def test_floater_test_api(client, secret_key, admin_key, new_floater_config):
    """The Api is now verified good to go and tests can interact with it"""
    fc = new_floater_config[0]
    floaterconfig_id = fc.id
    assert client.floater_config.get_by_id(floaterconfig_id) == fc
    assert client.floater_config.get(filter_by=[client.filter.floater_config.id == fc.id])[0] == fc

    len_get_floater_config = 0
    cmp_ids = set([fc_i.campaign_id for fc_i in new_floater_config])
    for cmp_id in cmp_ids:
        len_get_floater_config += len(
            client.floater_config.get(filter_by=[
                client.filter.floater_config.campaign_id == cmp_id
            ]))
    assert len_get_floater_config == len(new_floater_config)

    category = random.choice(["current force",
                              "wind force",
                              "decay",
                              "regular wave",
                              "irregular wave",
                              "pull out",
                              "vim",
                              "freak wave"
                              ])
    orientation = random_lower_int()
    number = random_int()
    description = random_lower_string()
    test_date = str(datetime.now())
    campaign_id = fc.campaign_id
    floater_test = client.floater_test.create(number=number, description=description, test_date=test_date,
                                              campaign_id=campaign_id, category=category, orientation=orientation,
                                              floaterconfig_id=floaterconfig_id)
    assert client.floater_test.get_by_number(number)
    tests = client.test.get(filter_by=[
        client.filter.test.number == number,
        client.filter.test.description == description],
        sort_by=[client.sort.test.test_date.asc])
    assert len(tests) == 1
    assert tests[0] == client.test.get_by_id(tests[0].id)
    assert tests[0] in client.test.get_by_number(number)
    assert len(client.test.get_by_number('not existing name')) == 0
    tests_check = client.test.get(filter_by=[
        client.filter.test.campaign_id == campaign_id,
    ])
    assert len(tests_check) == 1
    floater_test_with_same_name = client.floater_test.create(number=number, description='description',
                                                             test_date=test_date, campaign_id=campaign_id,
                                                             category=category, orientation=orientation,
                                                             floaterconfig_id=floaterconfig_id)
    assert floater_test_with_same_name.id != floater_test.id
    assert client.test.get_by_id(floater_test.id) in client.test.get_by_number(number)
    assert client.test.get_by_id(floater_test_with_same_name.id) in client.test.get_by_number(number)
    assert client.test.get_by_id(floater_test.id) in client.floater_test.get_by_number(number)
    assert client.test.get_by_id(floater_test_with_same_name.id) in client.floater_test.get_by_number(number)

    test_fromcampaign = client.test.get_by_campaign_id(campaign_id)
    assert len(test_fromcampaign) == 2

    tests_check = client.floater_test.get(filter_by=[
        client.filter.floater_test.campaign_id == campaign_id
    ])

    assert len(tests_check) == 2
    for i in test_fromcampaign:
        assert i in tests_check

    all_floater_tests = client.floater_test.get()
    assert len(all_floater_tests) >= len(tests_check)

    assert not client.test.get_by_number(94493)
    assert not client.floater_test.get_by_number(94439)

    client.test.delete(floater_test.id, secret_key=secret_key)
    client.test.delete(floater_test_with_same_name.id, secret_key=secret_key)


def test_wave_calibration_api(client, secret_key, admin_key, new_campaigns):
    """The Api is now verified good to go and tests can interact with it"""
    camp = new_campaigns[0]
    wave_spectrum = random.choice(["jonswap",
                                   "torsethaugen",
                                   "broad band",
                                   "chirp wave",
                                   "regular",
                                   None])
    wave_height = random_float()
    wave_period = random_float()
    gamma = random_float()
    wave_direction = random_float()
    current_velocity = random_float()
    current_direction = random_float()
    campaign_id = camp.id
    number = random_int()
    description = random_lower_string()
    test_date = str(datetime.now())

    wavecal = client.wave_calibration.create(number=number, description=description, test_date=test_date,
                                             campaign_id=campaign_id, wave_spectrum=wave_spectrum,
                                             wave_height=wave_height, wave_period=wave_period, gamma=gamma,
                                             wave_direction=wave_direction, current_velocity=current_velocity,
                                             current_direction=current_direction)

    assert client.wave_calibration.get_by_number(number)
    tests = client.test.get(filter_by=[
        client.filter.test.number == number,
        client.filter.test.description == description],
        sort_by=[client.sort.test.test_date.asc])
    assert len(tests) == 1
    assert tests[0] == client.test.get_by_id(tests[0].id)
    assert tests[0] in client.test.get_by_number(number)
    assert len(client.test.get_by_number('not existing name')) == 0
    assert len(client.wave_calibration.get_by_number('not existing name')) == 0

    assert tests[0] in client.wave_calibration.get_by_number(number)
    tests_check = client.test.get(filter_by=[client.filter.test.campaign_id == campaign_id])
    assert tests[0] in tests_check

    tests_check_wavecal = client.wave_calibration.get(filter_by=[
        client.filter.wave_calibration.campaign_id == campaign_id
    ])
    assert len(tests_check_wavecal) == 1
    test_from_campaign = client.test.get_by_campaign_id(campaign_id).filter(type="Wave Calibration")
    assert len(test_from_campaign) == 1

    all_wave_cal_tests = client.test.get()
    assert len(all_wave_cal_tests) >= len(tests_check_wavecal)

    wavecal_samename = client.wave_calibration.create(number=number, description='description', test_date=test_date,
                                                      campaign_id=campaign_id, wave_spectrum=wave_spectrum,
                                                      wave_height=wave_height, wave_period=wave_period, gamma=gamma,
                                                      wave_direction=wave_direction, current_velocity=current_velocity,
                                                      current_direction=current_direction)
    assert wavecal_samename.id != wavecal.id
    assert client.test.get_by_id(wavecal.id) in client.test.get_by_number(number)
    assert client.test.get_by_id(wavecal_samename.id) in client.test.get_by_number(number)
    assert client.test.get_by_id(wavecal.id) in client.wave_calibration.get_by_number(number)
    assert client.test.get_by_id(wavecal_samename.id) in client.wave_calibration.get_by_number(number)

    test_fromcampaign = client.test.get_by_campaign_id(campaign_id)
    assert tests[0] in test_fromcampaign

    client.test.delete(wavecal.id, secret_key=secret_key)
    client.test.delete(wavecal_samename.id, secret_key=secret_key)


def test_wind_calibration_test_api(client, secret_key, admin_key, new_campaigns):
    """The Api is now verified good to go and tests can interact with it"""
    camp = new_campaigns[0]
    wind_spectrum = random_lower_short_string()
    wind_velocity = random_float()
    zref = random_float()
    wind_direction = random_float()
    campaign_id = camp.id
    number = random_int()
    description = random_lower_string()
    test_date = str(datetime.now())

    windcal = client.wind_calibration.create(number=number, description=description, test_date=test_date,
                                             campaign_id=campaign_id, wind_spectrum=wind_spectrum,
                                             wind_velocity=wind_velocity, zref=zref, wind_direction=wind_direction)

    assert client.wind_calibration.get_by_number(number)
    tests = client.test.get(filter_by=[
        client.filter.test.number == number,
        client.filter.test.description == description],
        sort_by=[client.sort.test.test_date.asc])
    assert len(tests) == 1
    assert tests[0] == client.test.get_by_id(tests[0].id)
    assert tests[0] in client.test.get_by_number(number)
    assert len(client.test.get_by_number('not existing name')) == 0
    assert len(client.wind_calibration.get_by_number('not existing name')) == 0

    tests_check = client.test.get(filter_by=[
        client.filter.test.campaign_id == campaign_id,
    ])
    assert tests[0] in tests_check
    tests_check_windcal = client.wind_calibration.get(filter_by=[
        client.filter.wind_calibration.campaign_id == campaign_id,
    ])
    assert tests[0] in tests_check_windcal
    windcal_samename = client.wind_calibration.create(number=number, description='description', test_date=test_date,
                                                      campaign_id=campaign_id, wind_spectrum=wind_spectrum,
                                                      wind_velocity=wind_velocity, zref=zref,
                                                      wind_direction=wind_direction)
    assert windcal_samename.id != windcal.id
    assert client.test.get_by_id(windcal.id) in client.test.get_by_number(number)
    assert client.test.get_by_id(windcal_samename.id) in client.test.get_by_number(number)
    assert client.test.get_by_id(windcal.id) in client.wind_calibration.get_by_number(number)
    assert client.test.get_by_id(windcal_samename.id) in client.wind_calibration.get_by_number(number)

    test_from_campaign = client.test.get_by_campaign_id(campaign_id)
    assert tests[0] in test_from_campaign

    all_wind_cal_test = client.wind_calibration.get()
    assert len(all_wind_cal_test) >= len(test_from_campaign)

    client.test.delete(windcal.id, secret_key=secret_key)
    client.test.delete(windcal_samename.id, secret_key=secret_key)


def test_test_resources(client, secret_key, admin_key, new_tests, new_timeseries):
    test = new_tests[0]
    ts = test.timeseries()[0]
    assert ts == test.timeseries(sensor_id=ts.sensor_id)


def test_test_limit_skip(client, new_tests):
    all_tests = client.test.get(limit=10000)

    portion = max(1, len(all_tests) // 5)
    part_of_tests = client.test.get(limit=portion, skip=0)
    assert len(part_of_tests) == portion

    n_skips = -(len(all_tests) // -portion)  # ceiling divide

    all_tests_in_steps = []
    for skip in range(n_skips):
        all_tests_in_steps.extend(client.test.get(limit=portion, skip=skip * portion))

    assert len(all_tests_in_steps) == len(all_tests)
    for test in all_tests:
        assert test in all_tests_in_steps
