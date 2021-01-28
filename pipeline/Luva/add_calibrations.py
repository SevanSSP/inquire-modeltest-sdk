import os
from scipy.io import loadmat
from modeltestSDK import Client
from modeltestSDK.resources import Campaign
from .add_timeseries import read_datapoints
import re


def add_calibrations(campaign: Campaign, client: Client = None):
    os.chdir("C://Users/jen.SEVAN/Documents/529 Luva_2009/Analysis/Timeseries (To be modified)/Current/Calib")
    add_current_calibrations(campaign=campaign,client=client)
    os.chdir("C://Users/jen.SEVAN/Documents/529 Luva_2009/Analysis/Timeseries (To be modified)/Wind/Calib")
    add_wind_calibrations(campaign=campaign,client=client)
    os.chdir("C://Users/jen.SEVAN/Documents/529 Luva_2009/Analysis/Timeseries (To be modified)/IrrWave/WaveCalib")
    add_wave_calibrations(campaign=campaign,client=client)


def add_wind_calibrations(campaign: Campaign, client: Client = None):
    wind_calibrations = dict()
    calibrations = os.listdir(path='.')
    for calibration in calibrations:
        calibration_data = loadmat(os.getcwd() + "\\" + calibration)
        calibration_description = str(calibration_data['comment'])[2:-2]
        calibration_number = str(calibration_data['test_num'][0])[1:-1]
        calibration_date = str(calibration_data['test_date'])[2:-2]
        wind_vel_str = re.findall(r"U\d+\d+", calibration_description)[0]
        wind_vel = float(wind_vel_str.replace('U', ''))

        wind_calibration = client.wind_calibration.create(number=calibration_number,
                                                          description=calibration_description,
                                                          test_date=calibration_date,
                                                          campaign_id=campaign.id,
                                                          wind_spectrum='NPD',
                                                          wind_velocity=wind_vel,
                                                          zref=20,
                                                          wind_direction=0,
                                                          read_only=True)

        read_datapoints(data=calibration_data, test=wind_calibration, client=client)

        wind_calibrations[calibration_number] = wind_calibration.id
    return wind_calibrations


def add_current_calibrations(campaign: Campaign, client: Client = None):
    calibration = os.listdir(path='.')[0]
    calibration_data = loadmat(os.getcwd() + "\\" + calibration)
    calibration_description = str(calibration_data['comment'])[2:-2]
    calibration_number = str(calibration_data['test_num'][0])[1:-1]
    calibration_date = str(calibration_data['test_date'])[2:-2]
    current_vel_str = re.findall(r"\d+,\d+", calibration_description)[0]
    current_vel = float(current_vel_str.replace(',', '.'))

    current_calibration = client.wave_calibration.create(number=calibration_number,
                                                         description=calibration_description,
                                                         test_date=calibration_date,
                                                         campaign_id=campaign.id,
                                                         wave_spectrum="jonswap",
                                                         wave_height=0,
                                                         wave_period=0,
                                                         gamma=0,
                                                         wave_direction=0,
                                                         current_velocity=current_vel,
                                                         current_direction=0,
                                                         read_only=True, )
    read_datapoints(data=calibration_data, test=current_calibration, client=client)

    return current_calibration.id


def add_wave_calibrations(campaign: Campaign, client: Client = None):

    calibrations = os.listdir(path='.')
    for calibration in calibrations:
        calibration_data = loadmat(os.getcwd() + "\\" + calibration)
        calibration_description = str(calibration_data['comment'])[2:-2]
        calibration_number = str(calibration_data['test_num'][0])[1:-1]
        calibration_date = str(calibration_data['test_date'])[2:-2]

        res = re.findall(r'H[-+]?[0-9]*\.?[0-9]+', calibration_description)
        if res:
            wave_height = float(res[0][1:])
        else:
            raise KeyError("Wave height not found")
        res = re.findall(r'T[-+]?[0-9]*\.?[0-9]+', calibration_description)
        if res:
            wave_period = float(res[0][1:])
        else:
            raise KeyError("Wave period not found")
        res = re.findall(r'C[-+]?[0-9]*\.?[0-9]+', calibration_description)
        if res:
            current_vel = float(res[0][1:])
        else:
            current_vel = 0
        if calibration_description.find("IRR") == -1:
            wave_spectrum = "regular"
            gamma = 0
        else:
            wave_spectrum="jonswap"
            gamma = 3.3

        wave_calibration = client.wave_calibration.create(number=calibration_number,
                                                          description=calibration_description,
                                                          test_date=calibration_date,
                                                          campaign_id=campaign.id,
                                                          wave_spectrum=wave_spectrum,
                                                          wave_height=wave_height,
                                                          wave_period=wave_period,
                                                          gamma=gamma,
                                                          wave_direction=0,
                                                          current_velocity=current_vel,
                                                          current_direction=0,
                                                          read_only=True, )
        client.tag.create(name='comment', comment='Gamma unknown, 3.3 assumed', test_id=wave_calibration.id)
        read_datapoints(data=calibration_data, test=wave_calibration, client=client)

