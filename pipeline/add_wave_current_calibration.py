import datetime
from modeltestSDK.resources import Campaign, Test, Floater, WaveCurrentCalibration, WindConditionCalibration
from modeltestSDK.client import SDKclient
from pipeline.add_timeseries import read_datapoints_from_csv_with_pandas
import os
from modeltestSDK.utils import get_datetime_date, get_parent_dir


def add_wave_current_calibrations(campaign_dir: str, campaign: Campaign, client: SDKclient):

    os.chdir(campaign_dir)
    os.chdir(os.getcwd() + "\\" + "WaveCalib")
    calibs = os.listdir(path='.')
    for calib in calibs:
        # find wave spectrum and wave height+period
        wave_spectrum = calib.split("_")[0]
        if wave_spectrum == "Irreg":
            wave_spectrum = "jonswap"  # jonswap er forsøkt tilnærmet i SWACH testene
        if wave_spectrum == "Reg":
            wave_spectrum = "regular"
        wave_height = calib.split("_")[1]
        wave_height = float(wave_height.split("s")[1])
        wave_period = calib.split("_")[2]
        wave_period = float(wave_period.split("p")[1])
        measured_hs = wave_height  # midlertidig
        measured_tp = wave_period  # midlertidig #TODO: Lese inn calibration
        gamma = find_gamma(measured_hs, measured_tp)

        # find test date and time
        os.chdir(os.getcwd() + "\\" + calib)
        times = os.listdir(path='.')
        date = times[0].split(" ")[1]
        timestamp = times[0].split(" ")[2]
        date_time = date + timestamp

        wave_current_calibration = client.wave_current_calibration.create(description=calib,
                                                                          test_date=get_datetime_date(date_time),
                                                                          campaign_id=campaign.id,
                                                                          measured_hs=measured_hs,
                                                                          measured_tp=measured_tp,
                                                                          wave_spectrum=wave_spectrum,
                                                                          wave_period=wave_period,
                                                                          wave_height=wave_height,
                                                                          gamma=gamma,  # TODO: Add gamma
                                                                          wave_direction=0,
                                                                          current_velocity=0,
                                                                          current_direction=0)

        for time in times:
            os.chdir(os.getcwd() + "\\" + time)
            file = [os.getcwd() + "\\" + x for x in os.listdir(path='.') if x.split(" ")[0] == time.split(" ")[0]]
            read_datapoints_from_csv_with_pandas(file=file, test_id=wave_current_calibration.id, client=client)
            os.chdir(get_parent_dir(os.getcwd()))
        os.chdir(get_parent_dir(os.getcwd()))



        return wave_current_calibration


def find_gamma(Hs, Tp):
    if Hs == 7.0 and Tp == 12.0:
        gamma = 2.0
    elif Hs == 7.0 and Tp == 16.0:
        gamma = 2.0
    elif Hs == 10.0 and Tp == 13.0:
        gamma = 3.0
    elif Hs == 10.0 and Tp == 16.0:
        gamma = 3.0
    else:  # Hs==15.0 and Tp==16.0: # ifølge specs er det 15.6 og ikke 15.0
        gamma = 2.8
        raise Warning("Gamma might be wrong")
    return gamma