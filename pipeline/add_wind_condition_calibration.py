import datetime
from modeltestSDK.resources import Campaign, Test, Floater, WaveCurrentCalibration, WindConditionCalibration
from modeltestSDK.client import SDKclient
from pipeline.add_timeseries import read_datapoints_from_csv_with_pandas
import os
from modeltestSDK.utils import get_datetime_date, get_parent_dir

def add_wind_condition_calibrations(client: SDKclient, campaign: Campaign):

    wind_condition_calibration = client.wind_condition_calibration.create(test_name='test with no wind',
                                                                          test_date=get_datetime_date('180120 173446'), # en random dato
                                                                          campaign_id=campaign.id,
                                                                          measured_hs=10,  # random verdi
                                                                          measured_tp=10,  # random verdi
                                                                          wind_spectrum=None,
                                                                          wind_velocity=None,
                                                                          wind_direction=None)

    return wind_condition_calibration