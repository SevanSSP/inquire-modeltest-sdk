from datetime import datetime
from tests.utils import random_lower_int, random_float, random_lower_short_string, random_lower_string, random_bool, \
    random_int
import random


def test_floatertest_api(client, secret_key, admin_key, new_floaterconfig):
    """The Api is now verified good to go and tests can interact with it"""
    fc = new_floaterconfig[0]
    floaterconfig_id = fc.id
    assert client.floaterconfig.get_by_id(floaterconfig_id) == fc
    assert client.floaterconfig.get(filter_by=[client.filter.floaterconfig.id == fc.id])[0] == fc

    len_get_floaterconfig = 0
    cmp_ids = set([fc_i.campaign_id for fc_i in new_floaterconfig])
    for cmp_id in cmp_ids:
        len_get_floaterconfig += len(
            client.floaterconfig.get(filter_by=[
                client.filter.floaterconfig.campaign_id == cmp_id
            ]))
    assert len_get_floaterconfig == len(new_floaterconfig)

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
    floatertest = client.floatertest.create(number=number, description=description, test_date=test_date,
                                            campaign_id=campaign_id, category=category, orientation=orientation,
                                            floaterconfig_id=floaterconfig_id)
    assert client.floatertest.get_by_number(number)
    tests = client.test.get(filter_by=[
        client.filter.test.number == number,
        client.filter.test.description == description],
        sort_by=[client.sort.test.test_date.asc])
    assert len(tests) == 1
    assert tests[0] == client.test.get_by_number(number) == client.test.get_by_id(tests[0].id)
    assert client.test.get_by_number('not existing name') is None
    tests_check = client.test.get(filter_by=[
        client.filter.test.campaign_id == campaign_id,
    ])
    assert len(tests_check) == 1
    floatertest_with_same_name = client.floatertest.create(number=number, description='description',
                                                           test_date=test_date, campaign_id=campaign_id,
                                                           category=category, orientation=orientation,
                                                           floaterconfig_id=floaterconfig_id)
    assert floatertest_with_same_name.id != floatertest.id
    assert client.test.get_by_number(number) == client.test.get_by_id(floatertest.id)
    assert client.test.get_by_number(number) != client.test.get_by_id(floatertest_with_same_name.id)
    assert client.floatertest.get_by_number(number) == client.test.get_by_id(floatertest.id)
    assert client.floatertest.get_by_number(number) != client.test.get_by_id(floatertest_with_same_name.id)
    test_fromcampaign = client.test.get_by_campaign_id(campaign_id)
    assert len(test_fromcampaign) == 2

    tests_check = client.floatertest.get(filter_by=[
        client.filter.floatertest.campaign_id == campaign_id
    ])

    assert len(tests_check) == 2
    for i in test_fromcampaign:
        assert i in tests_check

    assert not client.test.get_by_number(94493)
    assert not client.floatertest.get_by_number(94439)

    client.test.delete(floatertest.id, secret_key=secret_key)
    client.test.delete(floatertest_with_same_name.id, secret_key=secret_key)


def test_wavecalibrationtest_api(client, secret_key, admin_key, new_campaigns):
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

    wavecal = client.wavecalibration.create(number=number, description=description, test_date=test_date,
                                            campaign_id=campaign_id, wave_spectrum=wave_spectrum,
                                            wave_height=wave_height, wave_period=wave_period, gamma=gamma,
                                            wave_direction=wave_direction, current_velocity=current_velocity,
                                            current_direction=current_direction)

    assert client.wavecalibration.get_by_number(number)
    tests = client.test.get(filter_by=[
        client.filter.test.number == number,
        client.filter.test.description == description],
        sort_by=[client.sort.test.test_date.asc])
    assert len(tests) == 1
    assert tests[0] == client.test.get_by_number(number) == client.test.get_by_id(tests[0].id)
    assert client.test.get_by_number('not existing name') is None
    assert client.wavecalibration.get_by_number('not existing name') is None

    assert tests[0] == client.wavecalibration.get_by_number(number)
    tests_check = client.test.get(filter_by=[client.filter.test.campaign_id == campaign_id])
    assert len(tests_check) == 1
    tests_check_wavecal = client.wavecalibration.get(filter_by=[
        client.filter.wavecalibration.campaign_id == campaign_id
    ])
    assert len(tests_check_wavecal) == 1
    test_fromcampaign = client.test.get_by_campaign_id(campaign_id, test_type="Wave Calibration")
    assert len(test_fromcampaign) == 1

    wavecal_samename = client.wavecalibration.create(number=number, description='description', test_date=test_date,
                                                     campaign_id=campaign_id, wave_spectrum=wave_spectrum,
                                                     wave_height=wave_height, wave_period=wave_period, gamma=gamma,
                                                     wave_direction=wave_direction, current_velocity=current_velocity,
                                                     current_direction=current_direction)
    assert wavecal_samename.id != wavecal.id
    assert client.test.get_by_number(number) == client.test.get_by_id(wavecal.id)
    assert client.test.get_by_number(number) != client.test.get_by_id(wavecal_samename.id)
    assert client.wavecalibration.get_by_number(number) == client.test.get_by_id(wavecal.id)
    assert client.wavecalibration.get_by_number(number) != client.test.get_by_id(wavecal_samename.id)
    test_fromcampaign = client.test.get_by_campaign_id(campaign_id)
    assert len(test_fromcampaign) == 2
    client.test.delete(wavecal.id, secret_key=secret_key)
    client.test.delete(wavecal_samename.id, secret_key=secret_key)


def test_windcalibrationtest_api(client, secret_key, admin_key, new_campaigns):
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

    windcal = client.windcalibration.create(number=number, description=description, test_date=test_date,
                                            campaign_id=campaign_id, wind_spectrum=wind_spectrum,
                                            wind_velocity=wind_velocity, zref=zref, wind_direction=wind_direction)

    assert client.windcalibration.get_by_number(number)
    tests = client.test.get(filter_by=[
        client.filter.test.number == number,
        client.filter.test.description == description],
        sort_by=[client.sort.test.test_date.asc])
    assert len(tests) == 1
    assert tests[0] == client.test.get_by_number(number) == client.test.get_by_id(tests[0].id)
    assert client.test.get_by_number('not existing name') is None
    assert client.windcalibration.get_by_number('not existing name') is None

    tests_check = client.test.get(filter_by=[
        client.filter.test.campaign_id == campaign_id,
    ])
    assert len(tests_check) == 1
    tests_check_windcal = client.windcalibration.get(filter_by=[
        client.filter.windcalibration.campaign_id == campaign_id,
    ])
    assert len(tests_check_windcal) == 1
    windcal_samename = client.windcalibration.create(number=number, description='description', test_date=test_date,
                                                     campaign_id=campaign_id, wind_spectrum=wind_spectrum,
                                                     wind_velocity=wind_velocity, zref=zref,
                                                     wind_direction=wind_direction)
    assert windcal_samename.id != windcal.id
    assert client.test.get_by_number(number) == client.test.get_by_id(windcal.id)
    assert client.test.get_by_number(number) != client.test.get_by_id(windcal_samename.id)
    assert client.windcalibration.get_by_number(number) == client.test.get_by_id(windcal.id)
    assert client.windcalibration.get_by_number(number) != client.test.get_by_id(windcal_samename.id)
    test_fromcampaign = client.test.get_by_campaign_id(campaign_id)
    assert len(test_fromcampaign) == 2
    client.test.delete(windcal.id, secret_key=secret_key)
    client.test.delete(windcal_samename.id, secret_key=secret_key)


def test_test_resources(client, secret_key, admin_key, new_tests, new_timeseries):
    test = new_tests[0]
    ts = test.timeseries()[0]
    assert ts == test.timeseries(sensor_id=ts.sensor_id)
