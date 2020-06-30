import datetime
from modeltestSDK.resources import Campaign, Test, Floater, WaveCurrentCalibration, WindConditionCalibration
from modeltestSDK.client import SDKclient
from pipeline.add_timeseries import read_datapoints_from_csv_with_pandas


def add_floater_test(files, campaign: Campaign, testname: str, wave_current_calibration: WaveCurrentCalibration, wind_condition_calibration: WindConditionCalibration, date: datetime, concept_id: str, client: SDKclient):

    orientation = 0     # for alle i SWACH
    draft = 29.5        # Fra Specs

    x = testname.split("_")[0]
    # hardkoding av category basert på filnavn
    if x == "waveReg":
        category = "regular wave"
    elif x == "waveIrreg":
        category = "irregular wave"
    elif x[0:3] == "X30" or x[0:3] == "Y30" or x[0:3] == "X20" or x[0:3] == "Y20":
        category = "decay"
    elif x[0:3] == "X10":
        category = "pull out"

    floater_test = client.floater.create(description=testname,
                                         test_date=date,
                                         campaign_id=campaign.id,
                                         type="floater",
                                         measured_hs=10,    # en random verdi
                                         measured_tp=13,    # en random verdi
                                         category=category,
                                         orientation=orientation,
                                         draft=draft,
                                         wave_id=wave_current_calibration.id,
                                         wind_id=wind_condition_calibration.id)

    for file in files:
        read_datapoints_from_csv_with_pandas(file=file, test_id=floater_test.id)

    return floater_test
