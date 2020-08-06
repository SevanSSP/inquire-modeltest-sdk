from .utils import format_class_name
import warnings
from .resources import (Campaign, CampaignList, Test, TestList, Sensor, SensorList, Timeseries, TimeseriesList,
                        DataPoint, DataPointList, Floater, FloaterList, WaveCurrentCalibration,
                        WaveCurrentCalibrationList,
                        WindConditionCalibration, WindConditionCalibrationList)


def get_id_from_response(response):
    return response[0]["id"]


class BaseAPI:
    def __init__(self, client):
        self._resource_path = format_class_name(self.__class__.__name__)
        self.client = client


class NamedBaseAPI(BaseAPI):
    '''
    Only for database items with names. To retrieve id from name
    '''

    def get_id(self, name: str) -> str:
        response = self.client.get(format_class_name(self.__class__.__name__), "all", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return response[0]['id']
        else:
            raise Exception(f"Could not find any object with name {name}")


class CampaignAPI(NamedBaseAPI):

    def create(self, name: str, description: str, location: str, date: any, waterline_diameter: float,
               scale_factor: float, water_density: float, water_depth: float, transient: float) -> Campaign:
        body = dict(name=name, description=description, location=location, date=date, waterline_diameter=waterline_diameter,
                    scale_factor=scale_factor, water_density=water_density, water_depth=water_depth,
                    transient=transient)
        data = self.client.post(self._resource_path, body=body)
        return Campaign.from_dict(data=data, client=self.client)

    def get(self, id: str) -> Campaign:
        data = self.client.get(self._resource_path, id)
        return Campaign.from_dict(data=data, client=self.client)

    def get_by_name(self, name: str) -> Campaign:
        response = self.client.get(format_class_name(self.__class__.__name__), "all", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return Campaign.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {name}")

    def get_all(self) -> CampaignList:
        data = self.client.get(self._resource_path, "all")
        obj_list = [Campaign.from_dict(data=obj, client=self.client) for obj in data]
        return CampaignList(resources=obj_list, client=None)

    def delete(self, id: str):
        self.client.delete(self._resource_path, id)

    def patch(self, body: dict, id: str) -> Campaign:
        data = self.client.patch(self._resource_path, endpoint=f"{id}", body=body)
        return Campaign.from_dict(data=data, client=self.client)

    def get_sensors(self, id: str) -> SensorList:
        data = self.client.get(self._resource_path, f"{id}/sensors")
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def get_tests(self, id: str, type: str = None) -> TestList:
        data = self.client.get(self._resource_path, f"{id}/tests", parameters={"type": type})
        resources = [Test.from_dict(data=obj, client=self.client) for obj in data]
        return TestList(resources=resources, client=self.client)


class TestAPI(NamedBaseAPI):

    def get(self, id: str) -> Test:
        data = self.client.get(self._resource_path, id)
        return Test.from_dict(data=data, client=self.client)

    def delete(self, item_id: str):
        self.client.delete(self._resource_path, item_id)

    def get_timeseries(self, id: str) -> TimeseriesList:
        data = self.client.get(self._resource_path, f"{id}/timeseries")
        resources = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=resources, client=self.client)


class FloaterAPI(TestAPI):

    def create(self, description: str, test_date: str, campaign_id: str,
               # measured_hs: str, measured_tp: str,
               category: str, orientation: float, draft: float, wave_id: str = None, wind_id: str = None) -> Floater:
        body = dict(description=description, type="floater", test_date=test_date, campaign_id=campaign_id,  # measured_hs=measured_hs, measured_tp=measured_tp,
                    category=category, orientation=orientation, draft=draft, wave_id=wave_id,
                    wind_id=wind_id)
        data = self.client.post(self._resource_path, body=body)
        return Floater.from_dict(data=data, client=self.client)

    def get(self, id: str) -> Floater:
        data = self.client.get(self._resource_path, id)
        return Floater.from_dict(data=data, client=self.client)

    def get_by_name(self, description: str) -> Floater:
        response = self.client.get(format_class_name(self.__class__.__name__), "all",
                                   parameters={'description': description})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {description} returned several objects,"
                              f" first was returned")
            return Floater.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {description}")

    def get_all(self) -> FloaterList:
        data = self.client.get(self._resource_path, "all")
        obj_list = [Floater.from_dict(data=obj, client=self.client) for obj in data]
        return FloaterList(resources=obj_list, client=None)


class WaveCurrentCalibrationAPI(TestAPI):

    def create(self, description: str, test_date: str, campaign_id: str,
               wave_spectrum: str, wave_height: float, wave_period: float, gamma: float,
               wave_direction: float, current_velocity: float, current_direction: float,
               id: str = None) -> WaveCurrentCalibration:
        body = dict(description=description, type="waveCurrentCalibration", test_date=test_date,
                    campaign_id=campaign_id,  # measured_hs=measured_hs, measured_tp=measured_tp,
                    wave_spectrum=wave_spectrum, wave_period=wave_period, wave_height=wave_height,
                    gamma=gamma, wave_direction=wave_direction, current_velocity=current_velocity,
                    current_direction=current_direction, id=id)

        data = self.client.post(self._resource_path, body=body)
        return WaveCurrentCalibration.from_dict(data=data, client=self.client)

    def get(self, id: str) -> WaveCurrentCalibration:
        data = self.client.get(self._resource_path, id)
        return WaveCurrentCalibration.from_dict(data=data, client=self.client)

    def get_all(self) -> WaveCurrentCalibrationList:
        data = self.client.get(self._resource_path, "all")
        obj_list = [WaveCurrentCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WaveCurrentCalibrationList(resources=obj_list, client=None)


class WindConditionCalibrationAPI(TestAPI):

    def create(self, description: str, test_date: str, campaign_id: str,  # measured_hs: str, measured_tp: str,
               wind_spectrum: str, wind_velocity: float, zref: float, wind_direction: float,
               id: str = None) -> WindConditionCalibration:
        body = dict(description=description, test_date=test_date, type="windConditionCalibration",
                    campaign_id=campaign_id,
                    # measured_hs=measured_hs, measured_tp=measured_tp,
                    wind_spectrum=wind_spectrum,
                    wind_velocity=wind_velocity, zref=zref, wind_direction=wind_direction, id=id)

        data = self.client.post(self._resource_path, body=body)
        return WindConditionCalibration.from_dict(data=data, client=self.client)

    def get(self, id: str) -> WindConditionCalibration:
        data = self.client.get(self._resource_path, id)
        return WindConditionCalibration.from_dict(data=data, client=self.client)

    def get_all(self) -> WindConditionCalibrationList:
        data = self.client.get(self._resource_path, "all")
        obj_list = [WindConditionCalibration.from_dict(data=obj, client=self.client) for obj in data]
        return WindConditionCalibrationList(resources=obj_list, client=None)


class SensorAPI(NamedBaseAPI):

    def create(self, name: str, description: str, unit: str, kind: str, x: float, y: float, z: float,
               is_local: bool, campaign_id: str) -> Sensor:
        body = dict(name=name, description=description, unit=unit, kind=kind, x=x,
                    y=y, z=z, is_local=is_local, campaign_id=campaign_id)
        data = self.client.post(self._resource_path, body=body)
        return Sensor.from_dict(data=data, client=self.client)

    def get(self, id: str) -> Sensor:
        data = self.client.get(self._resource_path, id)
        return Sensor.from_dict(data=data, client=self.client)

    def get_multiple_by_name(self, ids) -> Sensor:
        return self.client.post(self._resource_path, "ids", body=ids)

    def get_by_name(self, name: str):
        response = self.client.get(format_class_name(self.__class__.__name__), "all", parameters={'name': name})
        if response:
            if len(response) != 1:
                warnings.warn(f"Searching {self.__class__.__name__} for name {name} returned several objects,"
                              f" first was returned")
            return Sensor.from_dict(data=response[0], client=self.client)
        else:
            raise Exception(f"Could not find any object with name {name}")

    def get_all(self) -> SensorList:
        data = self.client.get(self._resource_path, "all")
        obj_list = [Sensor.from_dict(data=obj, client=self.client) for obj in data]
        return SensorList(resources=obj_list, client=None)

    def delete(self, item_id: str):
        self.client.delete(self._resource_path, item_id)

    def patch(self, body: dict, sensor_id: str) -> Sensor:
        data = self.client.patch(self._resource_path, endpoint=f"{sensor_id}", body=body)
        return Sensor.from_dict(data=data, client=self.client)


class TimeseriesAPI(BaseAPI):

    def create(self, sensor_id: str, test_id: str) -> Timeseries:
        body = dict(sensor_id=sensor_id, test_id=test_id)
        data = self.client.post(self._resource_path, body=body)
        return Timeseries.from_dict(data=data, client=self.client)

    def get(self, id: str) -> Timeseries:
        data = self.client.get(self._resource_path, id)
        return Timeseries.from_dict(data=data, client=self.client)

    def get_all(self) -> TimeseriesList:
        data = self.client.get(self._resource_path, "all")
        obj_list = [Timeseries.from_dict(data=obj, client=self.client) for obj in data]
        return TimeseriesList(resources=obj_list, client=None)

    def delete(self, item_id: str):
        self.client.delete(self._resource_path, item_id)

    def patch(self, body: dict, id: str):
        return self.client.patch(resource=self._resource_path, endpoint=f"{id}", body=body)

    def get_data_points(self, id: str) -> DataPointList:
        data = self.client.get(resource=self._resource_path, endpoint=f"{id}/datapoints")
        if not data:
            return DataPointList(resources=[], client=self.client)

        resources = [DataPoint.from_dict(data=obj, client=self.client) for obj in data]
        return DataPointList(resources=resources, client=self.client)

    def post_data_points(self, id, body):
        data = self.client.post(resource="datapoint", endpoint="list", body=body)

    def get_standard_deviation(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/standarddeviation")
        return data

    def get_max_value(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/maxvalue")
        return data

    def get_min_value(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/minvalue")
        return data

    def get_measured_hs(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/measured_hs")
        return data

    def get_measured_tp(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/datapoints/measured_tp")
        return data

    def get_sensor(self, id: str):
        data = self.client.get(self._resource_path, f"{id}/sensor")
        return Sensor.from_dict(data=data, client=self.client)
