import os
import datetime
from modeltestSDK.resources import Campaign
from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date, get_parent_dir
from .add_timeseries import read_datapoints_from_csv_with_pandas

# It is recommended to open the file system for the STT campaign, to understand how calibration tests are added in order

def fill_campaign_with_wave_calibrations(campaign: Campaign, client: SDKclient, campaign_dir: str):

    # Add all wave_calibrations by iterating through wave calibration folders.
    os.chdir(campaign_dir)
    os.chdir(os.getcwd() + "\\" + "WaveCalib")
    calibrations = os.listdir(path='.')

    for calibration in calibrations:

        # Find wave spectrum, wave height and wave period based on file names
        # Example of file name: Irreg_Hs15_Tp16
        wave_spectrum = calibration.split("_")[0]
        if wave_spectrum == "Irreg":
            wave_spectrum = "jonswap"   # Jonswap is attempted to be created in STT campaign
        if wave_spectrum == "Reg":
            wave_spectrum = "regular"
        wave_height = calibration.split("_")[1]
        wave_height = float(wave_height.split("s")[1])
        wave_period = calibration.split("_")[2]
        wave_period = float(wave_period.split("p")[1])

        # Find gamma based on hs and tp pairs, based on values given in modeltest report
        gamma = find_gamma_based_on_hs_tp_pairs(wave_height, wave_period)

        os.chdir(os.getcwd() + "\\" + calibration)

        # Find test date and time from file name
        # Example of file name: WaveClibIrreg_Hs10_Tp16_nyTF 180120 145200
        times = os.listdir(path='.')
        date = times[0].split(" ")[1]
        timestamp = times[0].split(" ")[2]
        date_time = date + timestamp

        # Create wave&current calibration test in the database
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

        # Add all timeseries for every sensor used in the wave&current calibration test that was added
        for time in times:
            os.chdir(os.getcwd() + "\\" + time)

            # The .csv files that should be read have the same name as the calibration test. Only read these files.
            # Example of file name that should be read: WaveClibIrreg_Hs10_Tp16_nyTF Wagon 55
            files = [os.getcwd() + "\\" + x for x in os.listdir(path='.') if x.split(" ")[0] == time.split(" ")[0]]

            for file in files:
                read_datapoints_from_csv_with_pandas(file=file, test_id=wave_current_calibration.id, client=client)
            os.chdir(get_parent_dir(os.getcwd()))

        os.chdir(get_parent_dir(os.getcwd()))


# Find gamma based on Hs and Tp pairs. Values given in the STT reports.
def find_gamma_based_on_hs_tp_pairs(Hs, Tp):
    if Hs == 7.0 and Tp == 12.0:
        gamma = 2.0
    elif Hs == 7.0 and Tp == 16.0:
        gamma = 2.0
    elif Hs == 10.0 and Tp == 13.0:
        gamma = 3.0
    elif Hs == 10.0 and Tp == 16.0:
        gamma = 3.0
    elif Hs == 15.0 and Tp == 16.0:
        gamma = 2.8
    else:
        #Regular waves
        gamma = 0
    return gamma