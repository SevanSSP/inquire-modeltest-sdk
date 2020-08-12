import os
import datetime
from modeltestSDK.resources import Campaign, Test, DataPoint, WaveCurrentCalibration, WindConditionCalibration
from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date, get_parent_dir
from .add_timeseries import read_datapoints_from_csv_with_pandas
from .add_floater_test import add_floater_test
from .add_sensors import add_sensors


# Find gamma based on Hs and Tp pairs. Values given in the STT reports.
def find_gamma(Hs, Tp):
    if Hs == 7.0 and Tp == 12.0:
        gamma = 2.0
    elif Hs == 7.0 and Tp == 16.0:
        gamma = 2.0
    elif Hs == 10.0 and Tp == 13.0:
        gamma = 3.0
    elif Hs == 10.0 and Tp == 16.0:
        gamma = 3.0
    elif Hs == 15.0 and Tp == 16.0:  # Ifølge specs er det 15.6 og ikke 15.0
        gamma = 2.8
    else:
        #Regular waves
        gamma = 0
    return gamma




def fill_campaign(campaign: Campaign, concept_ids, client: SDKclient, campaign_dir: str):
    # Add all wave_calibrations by iterating through wave calibration folders.
    os.chdir(campaign_dir)
    os.chdir(os.getcwd() + "\\" + "WaveCalib")
    calibrations = os.listdir(path='.')
    for calibration in calibrations:
        # find wave spectrum and wave height+period based on file names
        wave_spectrum = calibration.split("_")[0]
        if wave_spectrum == "Irreg":
            wave_spectrum = "jonswap"  # jonswap er forsøkt tilnærmet i SWACH testene
        if wave_spectrum == "Reg":
            wave_spectrum = "regular"
        wave_height = calibration.split("_")[1]
        wave_height = float(wave_height.split("s")[1])
        wave_period = calibration.split("_")[2]
        wave_period = float(wave_period.split("p")[1])
        gamma = find_gamma(wave_height, wave_period)

        # find test date and time
        os.chdir(os.getcwd() + "\\" + calibration)
        times = os.listdir(path='.')
        date = times[0].split(" ")[1]
        timestamp = times[0].split(" ")[2]
        date_time = date + timestamp

        wave_current_calibration = client.wave_current_calibration.create(description=calibration,
                                                                          test_date=get_datetime_date(date_time),
                                                                          campaign_id=campaign.id,
                                                                          wave_spectrum=wave_spectrum,
                                                                          wave_period=wave_period,
                                                                          wave_height=wave_height,
                                                                          gamma=gamma,
                                                                          wave_direction=0,
                                                                          current_velocity=0,
                                                                          current_direction=0)

        for time in times:
            os.chdir(os.getcwd() + "\\" + time)
            files = [os.getcwd() + "\\" + x for x in os.listdir(path='.') if x.split(" ")[0] == time.split(" ")[0]]
            for file in files:
                read_datapoints_from_csv_with_pandas(file=file, test_id=wave_current_calibration.id,client=client)
            os.chdir(get_parent_dir(os.getcwd()))
        os.chdir(get_parent_dir(os.getcwd()))



    os.chdir(campaign_dir)
    for concept_id in concept_ids:
        os.chdir(campaign_dir + "\\" + concept_id)
        tests = os.listdir(path='.')
        for test in tests:
            os.chdir(os.getcwd() + "\\" + test)
            times = [x for x in os.listdir(path='.') if os.path.isdir(x)]
            date = times[0].split(" ")[1]  # Fetch the date from directory name
            timestamp = times[0].split(" ")[2]
            date_time = date + timestamp
            for time in times:
                os.chdir(os.getcwd() + "\\" + time)
                files = [os.getcwd() + "\\" + x for x in os.listdir(path='.') if
                         x.split(" ")[0] == test]  # Only add to test files if start with test name
                add_floater_test(files=files,
                                 campaign=campaign,
                                 testname=test,
                                 date=get_datetime_date(date_time),
                                 concept_id=concept_id,
                                 client=client)

                os.chdir(get_parent_dir(os.getcwd()))
            os.chdir(get_parent_dir(os.getcwd()))
        os.chdir(get_parent_dir(os.getcwd()))

