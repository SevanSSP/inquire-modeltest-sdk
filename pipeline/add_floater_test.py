import datetime
from modeltestSDK.resources import Campaign, Test, Floater, WaveCurrentCalibration, WindConditionCalibration
from modeltestSDK.client import SDKclient
from pipeline.add_timeseries import read_datapoints_from_csv_with_pandas
from modeltestSDK.utils import TwoWayDict

waveCalibDict = TwoWayDict()
waveCalibDict["waveIrreg_2101"] = "Irreg_Hs7_Tp12"
waveCalibDict["waveIrreg_2102"] = "Irreg_Hs7_Tp16"
waveCalibDict["waveIrreg_2103"] = "Irreg_Hs10_Tp13"
waveCalibDict["waveIrreg_2104"] = "Irreg_Hs10_Tp16"
waveCalibDict["waveIrreg_2105"] = "Irreg_Hs15_Tp16"
waveCalibDict["waveReg_1101"] = "Reg_Hs3_Tp6.5"
waveCalibDict["waveReg_1102"] = "Reg_Hs3_Tp8"
waveCalibDict["waveReg_1103"] = "Reg_Hs3_Tp8"
waveCalibDict["waveReg_1104"] = "Reg_Hs3_Tp10"
waveCalibDict["waveReg_1105"] = "Reg_Hs3_Tp10"
waveCalibDict["waveReg_1106"] = "Reg_Hs3_Tp13"
waveCalibDict["waveReg_1107"] = "Reg_Hs3_Tp13"
waveCalibDict["waveReg_1108"] = "Reg_Hs3_Tp15"


def add_floater_test(files, campaign: Campaign, testname: str, date: datetime, concept_id: str, client: SDKclient):
    orientation = 0  # for alle i SWACH
    draft = 29.5  # Fra Specs

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

    wave_id = client.wave_current_calibration.get_id(waveCalibDict(testname))

    floater_test = client.floater.create(description=testname,
                                         test_date=date,
                                         campaign_id=campaign.id,
                                         type="floater",
                                         measured_hs=10,  # en random verdi
                                         measured_tp=13,  # en random verdi
                                         category=category,
                                         orientation=orientation,
                                         draft=draft,
                                         wave_id=wave_id,
                                         wind_id=None)

    for file in files:
        print(file)
        read_datapoints_from_csv_with_pandas(file=file, test_id=floater_test.id, client=client)

    return floater_test
