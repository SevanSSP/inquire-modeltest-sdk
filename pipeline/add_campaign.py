import os
import datetime
from modeltestSDK.resources import Campaign, Test, DataPoint, WaveCurrentCondition, WindCurrentCondition
from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date, get_parent_dir

from .floater_test import add_floater_test


def fill_campaign(campaign: Campaign, concept_ids, client: SDKclient, campaign_dir: str):
    # Legg til alle wave_calibrations
    os.chdir(campaign_dir)
    os.chdir(os.getcwd() + "\\" + "WaveCalib")
    calibs = os.listdir(path='.')
    for calib in calibs:
        # find test date and time
        os.chdir(os.getcwd() + "\\" + calib)
        times = os.listdir(path='.')
        date = times[0].split(" ")[1]
        timestamp = times[0].split(" ")[2]
        date_time = date + timestamp
        os.chdir(get_parent_dir(os.getcwd()))

        wave_spectrum = calib.split("_")[0]
        if wave_spectrum == "Irreg":
            wave_spectrum = "jonswap"  # jonswap er forsøkt tilnærmet i SWACH testene
        if wave_spectrum == "Reg":
            wave_spectrum = "regular"
        wave_height = calib.split("_")[1]
        wave_height = float(wave_height.split("s")[1])
        wave_period = calib.split("_")[2]
        wave_period = float(wave_period.split("p")[1])
        print(wave_spectrum)
        print(wave_height)
        print(wave_period)
        measured_hs = wave_height  # midlertidig
        measured_tp = wave_period  # midlertidig #TODO: Lese inn calibration
        wave_current_calibration = client.waveCurrentCalibration.create(test_name=calib,
                                                                        test_date=get_datetime_date(date_time),
                                                                        campaign_id=campaign.id,
                                                                        measured_hs=measured_hs,
                                                                        measured_tp=measured_tp,
                                                                        wave_spectrum=wave_spectrum,
                                                                        wave_period=wave_period,
                                                                        wave_height=wave_height)
        #TODO: Må kunne skille mellom en wind calibration og wave calibration, ønsker ikke nødvendigvis å legge inn samtidig
        '''
        wind_calibration = client.windConditionCalibration.create(test_name=calib,
                                                                  test_date=get_datetime_date(date_time),
                                                                  campaign_id=campaign.id,
                                                                  measured_hs=10,  # random verdi
                                                                  measured_tp=10,  # random verdi
                                                                  wind_spectrum=None,
                                                                  wind_velocity=None,
                                                                  wind_direction=None)
        '''
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
                add_floater_test(files=files, campaign=campaign, testname=test, date=get_datetime_date(date_time),
                                 concept_id=concept_id)

                os.chdir(get_parent_dir(os.getcwd()))
            os.chdir(get_parent_dir(os.getcwd()))
        os.chdir(get_parent_dir(os.getcwd()))


def main():
    client = SDKclient()
    campaign_dir = "C:/Users/jen/Documents/STT"
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


if __name__ == "__main__":
    main()