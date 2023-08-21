from __future__ import annotations
from typing import Optional, Union
from .base import Resource, Resources
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .timeseries import TimeSeries
    from .sensor import Sensor
    from .test import FloaterTest, WindCalibration, WaveCalibration


class Tag(Resource):
    id: Optional[str]
    name: str
    comment: Optional[str]
    test_id: Optional[str]
    sensor_id: Optional[str]
    timeseries_id: Optional[str]

    @property
    def sensor(self) -> Union[Sensor, None]:
        if self.client and self.sensor_id:
            return self.client.sensor.get_by_id(self.sensor_id)
        else:
            return None

    @property
    def test(self) -> Union[FloaterTest, WindCalibration, WaveCalibration, None]:
        if self.client and self.test_id:
            test = self.client.test.get_by_id(self.test_id)
            print(test)
            if test.type == 'Floater Test':
                return self.client.floatertest.get_by_id(self.test_id)
            elif test.type == 'Wave Calibration':
                return self.client.wavecalibration.get_by_id(self.test_id)
            elif test.type == 'Wind Calibration':
                return self.client.windcalibration.get_by_id(self.test_id)
            else:
                raise ValueError('Unknown test type')
        else:
            return None

    @property
    def timeseries(self) -> Union[TimeSeries, None]:
        if self.client and self.timeseries_id:
            return self.client.timeseries.get_by_id(self.timeseries_id)
        else:
            return None


class Tags(Resources[Tag]):
    pass
