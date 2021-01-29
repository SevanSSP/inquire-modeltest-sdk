import pandas as pd
import datetime
from modeltestSDK.client import Client
from modeltestSDK.resources import SensorList, FloaterConfigList, WaveCalibrationList
from scipy.io import loadmat

client = Client()

xls_loc = "C://users/jen.SEVAN/Documents/ImportPipelineInput.xls"

df_campaign = pd.read_excel(xls_loc, sheet_name='Campaign', skiprows=2)
df_sensor = pd.read_excel(xls_loc, sheet_name='Sensor', skiprows=2, true_values="TRUE",false_values="FALSE")
df_sensor = df_sensor.fillna(value=0) # TODO: dangerous method use None?
df_floater_config = pd.read_excel(xls_loc, sheet_name='FloaterConfig', skiprows=2)
df_wave_calibration = pd.read_excel(xls_loc,sheet_name='WaveCal', skiprows=2)

restrict_access = True

for index, camp in df_campaign.iterrows():
    campaign = client.campaign.create(name=camp['name'],
                                      description=camp['description'],
                                      location=camp['location'],
                                      date=datetime.datetime(year=camp['year'], month=camp['month'], day=1).isoformat(),
                                      scale_factor=camp['scale_factor'],
                                      water_depth=camp['water_depth'],
                                      read_only=restrict_access)

sensors = SensorList(resources=[])

for index, sensor in df_sensor.iterrows():
    sensors.resources.append(
        client.sensor.create(name=sensor['name'],
                             description=sensor['description'],
                             unit=sensor['unit'],
                             kind=sensor['kind'],
                             x=sensor['x'],
                             y=sensor['y'],
                             z=sensor['z'],
                             is_local=sensor['is_local'],
                             campaign_id=campaign.id,
                             read_only=restrict_access)
    )

floater_configs = FloaterConfigList(resources=[])

for index, floater in df_floater_config.iterrows():
    floater_configs.resources.append(
        client.floater_config.create(name=floater['name'],
                                     description=floater['description'],
                                     campaign_id=campaign.id,
                                     draft=floater['draft'],
                                     characteristic_length=floater['characteristic_length'],
                                     read_only=restrict_access)
    )

wave_calibrations = WaveCalibrationList(resources=[])

for index, wave_cal in df_wave_calibration.iterrows():
    campain_folder = "C://users/jen.SEVAN/documents/"
    test_prefix = 'test'
    test_suffix = ''
    filename = test_prefix + str(wave_cal['number']) + test_suffix
    try:
        remaining_channels = dict()
        data = loadmat(campain_folder+filename, mdict=remaining_channels)
    except FileNotFoundError:
        raise FileNotFoundError(f"Wave calibration {wave_cal['number']} not found in folder {campain_folder}")

    if wave_cal["description"] == '*':
        description = data['description']
    else:
        description = wave_cal["description"]
    if wave_cal["test_date"] == '*':
        test_date = data['date'][0][0]
    else:
        test_date = wave_cal["test_date"]

