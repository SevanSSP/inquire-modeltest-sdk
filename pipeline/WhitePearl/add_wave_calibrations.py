import os
import datetime
from modeltestSDK.resources import Campaign
from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date, get_parent_dir
from .add_timeseries import read_datapoints_from_csv_with_pandas

def fill_campaign_with_wave_calibrations(campaign: Campaign, client: SDKclient, campaign_dir: str):

    client.wave_calibration.create(description="1-yr wave",
                                   test_date=campaign.date,
                                   campaign_id=campaign.id,
                                   wave_spectrum=,
                                   wave_period=wave_period,
                                   wave_height=wave_height,
                                   gamma=gamma,
                                   wave_direction=0,
                                   current_velocity=0,
                                   current_direction=0,
                                   read_only=True)

    client.wave_calibration.create(description=calibration,
                                   test_date=get_datetime_date(date_time),
                                   campaign_id=campaign.id,
                                   wave_spectrum=wave_spectrum,
                                   wave_period=wave_period,
                                   wave_height=wave_height,
                                   gamma=gamma,
                                   wave_direction=0,
                                   current_velocity=0,
                                   current_direction=0,
                                   read_only=True)

    client.wave_calibration.create(description=calibration,
                                   test_date=get_datetime_date(date_time),
                                   campaign_id=campaign.id,
                                   wave_spectrum=wave_spectrum,
                                   wave_period=wave_period,
                                   wave_height=wave_height,
                                   gamma=gamma,
                                   wave_direction=0,
                                   current_velocity=0,
                                   current_direction=0,
                                   read_only=True)