import os
import datetime
from modeltestSDK.utils import get_datetime_date, get_parent_dir
from modeltestSDK.resources import Campaign
from modeltestSDK.client import SDKclient
from pipeline.STT.add_timeseries import read_datapoints_from_csv_with_pandas
from modeltestSDK.utils import TwoWayDict

# It is recommended to open the file system for the STT campaign, to understand how floater tests are added in order


def fill_campaign_with_floater_tests(campaign: Campaign, concept_ids, client: SDKclient, campaign_dir: str):
    os.chdir(campaign_dir)

    # Go through system of files to add every floater test
    for concept_id in concept_ids:
        os.chdir(campaign_dir + "\\" + concept_id)
        tests = os.listdir(path='.')

        # tests is now a list with names of the folder for each test.
        # Example of name for a test folder: waveReg_1110
        for test in tests:
            os.chdir(os.getcwd() + "\\" + test)
            times = [x for x in os.listdir(path='.') if os.path.isdir(x)]
            # Example of name of folder that gives test date: waveReg_1110 220120 122654
            date = times[0].split(" ")[1]
            timestamp = times[0].split(" ")[2]
            date_time = date + timestamp

            for time in times:
                os.chdir(os.getcwd() + "\\" + time)

                # Only add to test files if start with test name
                # Example of file that should be added: waveReg_1110 Wagon 55
                files = [os.getcwd() + "\\" + x for x in os.listdir(path='.') if x.split(" ")[0] == test]

                # This method adds the floater test to the database, and also adds all timeseries for that test.
                add_floater_test(files=files,
                                 campaign=campaign,
                                 testname=test,
                                 date=get_datetime_date(date_time),
                                 concept_id=concept_id,
                                 client=client)

                os.chdir(get_parent_dir(os.getcwd()))
            os.chdir(get_parent_dir(os.getcwd()))
        os.chdir(get_parent_dir(os.getcwd()))


waveCalibDict = TwoWayDict()
waveCalibDict["waveIrreg_2101"] = "Irreg_Hs7_Tp12"
waveCalibDict["waveIrreg_2102"] = "Irreg_Hs7_Tp16"
waveCalibDict["waveIrreg_2103"] = "Irreg_Hs10_Tp13"
waveCalibDict["waveIrreg_2104"] = "Irreg_Hs10_Tp16"
waveCalibDict["waveIrreg_2105"] = "Irreg_Hs15_Tp16"
waveCalibDict["waveReg_1101"] = "Reg_Hs3_Tp6.5"
waveCalibDict["waveReg_1102"] = "Reg_Hs3_Tp8"
waveCalibDict["waveReg_1103"] = "Reg_Hs5_Tp8"
waveCalibDict["waveReg_1104"] = "Reg_Hs5_Tp10"
waveCalibDict["waveReg_1105"] = "Reg_Hs7_Tp10"
waveCalibDict["waveReg_1106"] = "Reg_Hs7_Tp13"
waveCalibDict["waveReg_1107"] = "Reg_Hs10_Tp13"
waveCalibDict["waveReg_1108"] = "Reg_Hs10_Tp15"
waveCalibDict["waveReg_1109"] = "Reg_Hs10_Tp17"
waveCalibDict["waveReg_1110"] = "Reg_Hs10_Tp25"
waveCalibDict["waveIrreg_2201"] = "Irreg_Hs7_Tp12"
waveCalibDict["waveIrreg_2202"] = "Irreg_Hs7_Tp16"
waveCalibDict["waveIrreg_2203"] = "Irreg_Hs10_Tp13"
waveCalibDict["waveIrreg_2204"] = "Irreg_Hs10_Tp16"
waveCalibDict["waveIrreg_2205"] = "Irreg_Hs15_Tp16"
waveCalibDict["waveReg_1201"] = "Reg_Hs3_Tp6.5"
waveCalibDict["waveReg_1202"] = "Reg_Hs3_Tp8"
waveCalibDict["waveReg_1203"] = "Reg_Hs5_Tp8"
waveCalibDict["waveReg_1204"] = "Reg_Hs5_Tp10"
waveCalibDict["waveReg_1205"] = "Reg_Hs7_Tp10"
waveCalibDict["waveReg_1206"] = "Reg_Hs7_Tp13"
waveCalibDict["waveReg_1207"] = "Reg_Hs10_Tp13"
waveCalibDict["waveReg_1208"] = "Reg_Hs10_Tp15"
waveCalibDict["waveReg_1209"] = "Reg_Hs10_Tp17"
waveCalibDict["waveReg_1210"] = "Reg_Hs10_Tp25"


def add_floater_test(files, campaign: Campaign, testname: str, date: datetime, concept_id: str, client: SDKclient):

    orientation = 0  # Standard for all floaters in SWACH modeltest
    if concept_id == "M206":
        draft = 29.5
    if concept_id == "M207":
        draft = 18

    x = testname.split("_")[0]
    # Hardcoding of category based on filename
    if x == "waveReg":
        category = "regular wave"
    elif x == "waveIrreg":
        category = "irregular wave"
    elif x[0:3] == "X30" or x[0:3] == "Y30" or x[0:3] == "X20" or x[0:3] == "Y20":
        category = "decay"
    elif x[0:3] == "X10":
        category = "pull out"

    # Connect floater test to the right wave calibration, if there is one.
    try:
        wave_id = client.wave_current_calibration.get_id(waveCalibDict[testname])
    except:
        wave_id = None

    # Create floater test in database
    floater_test = client.floater.create(description=testname,
                                         test_date=date,
                                         campaign_id=campaign.id,
                                         category=category,
                                         orientation=orientation,
                                         draft=draft,
                                         wave_id=wave_id,
                                         wind_id=None)  # No wind in STT campaign

    # Add every timeseries from the floater test
    for file in files:
        read_datapoints_from_csv_with_pandas(file=file, test_id=floater_test.id, client=client)
