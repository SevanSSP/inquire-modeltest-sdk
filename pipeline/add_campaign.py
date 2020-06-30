import os
import datetime
from modeltestSDK.resources import Campaign, Test, DataPoint, WaveCurrentCalibration, WindConditionCalibration
from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date, get_parent_dir
from .add_timeseries import read_datapoints_from_csv_with_pandas
from .add_floater_test import add_floater_test
from .add_sensors import add_sensors
from .add_wave_current_calibration import add_wave_current_calibrations
from .add_wind_condition_calibration import add_wind_condition_calibrations


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


# TODO: Koble riktig wave+wind calibration til floater som opprettes
#
def fill_campaign(campaign: Campaign, concept_ids, client: SDKclient, campaign_dir: str):
    # Legg til alle wave_calibrations. Foreløpig ligger også wind calibrations i metoden under
    wave_current_calibration = add_wave_current_calibrations(campaign_dir=campaign_dir, campaign=campaign, client=client)

    wind_condition_calibration = add_wind_condition_calibrations(client=client, campaign=campaign)


    # legg til alle floater testene
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
                # print("FILES: ", files, campaign_id, get_datetime_date(date_time))
                floater_test = add_floater_test(files=files,
                                                campaign=campaign,
                                                wave_current_calibration=wave_current_calibration,
                                                wind_condition_calibration=wind_condition_calibration,
                                                testname=test,
                                                date=get_datetime_date(date_time),
                                                concept_id=concept_id)

                os.chdir(get_parent_dir(os.getcwd()))
            os.chdir(get_parent_dir(os.getcwd()))
        os.chdir(get_parent_dir(os.getcwd()))


def main():
    client = SDKclient()
    campaign_dir = "C:/Users/nbu/Documents/SWACH"
    campaign = client.campaign.create(name=campaign_dir.split("/")[-1],
                                      description="Modeltest for SWACH",
                                      date=get_datetime_date("180120120000"),
                                      location="STADT TOWING TANK",
                                      diameter=70,  # main hull cylinder
                                      scale_factor=75,  # står i rapporten
                                      water_density=1025,  # usikkert
                                      water_depth=300,  # står kun >300
                                      transient=3 * 60 * 60)  # 3 hours in seconds)
    concept_ids = ["M206", "M207"]
    fill_campaign(campaign, concept_ids, client, campaign_dir)

    add_sensors(campaign, client)


if __name__ == "__main__":
    main()
