import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from qats import TimeSeries as QatsTimeseries
from .base import Resource, Resources


class DataPoints(Resource):
    time: List[float]
    value: List[float]
    timeseries_id: str

    def __len__(self):
        return len(self.time)

    @property
    def timeseries(self):
        if self.client:
            return self.client.timeseries.get_by_id(self.timeseries_id)
        else:
            return None

    def plot(self, show: bool = True, **kwargs):
        """
        Plot the datapoints.

        Parameters
        ----------
        show : bool, default True
            Whether to show the plot
        kwargs
            See pandas.DataFrame.plot for options.
        """
        # Set the x-axis label to "Time [s]" if not specified in the additional arguments
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = 'Time [s]'

        # set the y-axis label based on the kind and unit if not specified in the additional arguments
        if 'ylabel' not in kwargs:
            try:
                kwargs['ylabel'] = f'{self.timeseries.sensor.kind.capitalize()} [{self.timeseries.sensor.unit}]'
            except AttributeError:
                pass

        self.to_pandas().plot(**kwargs)
        if show:
            plt.show()

    def to_pandas(self) -> pd.DataFrame:
        """
        Convert the instance into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.

        See Also
        --------
        See keyword arguments on pydantic.BaseModel.dict()
        """
        try:
            sensor = self.timeseries.sensor
            test = self.timeseries.test
        except AttributeError:
            columns = None
        else:
            columns = [f'{test.number} - {sensor.name}']
        return pd.DataFrame(data=self.value, index=self.time, columns=columns)

    def to_qats_ts(self) -> QatsTimeseries:
        try:
            sensor = self.timeseries.sensor
            test = self.timeseries.test
        except AttributeError:
            name = 'unknown'
            kind = None
            unit = None
        else:
            name = f'{test.number} - {sensor.name}'
            kind = sensor.kind
            unit = sensor.unit
        return QatsTimeseries(name=name, x=np.array(self.value), t=np.array(self.time),
                              kind=kind, unit=unit)

    def create(self, **kwargs):
        print('## Datapoints are created through the Timeseries API / resource')


class DataPointsList(Resources[DataPoints]):

    def plot(self, show: bool = True, **kwargs):
        """
        Plot data points.

        Parameters
        ----------
        show : bool, default True
            Whether to show the plot
        kwargs
            See pandas.DataFrame.plot for options
        """

        # Set the x-axis label to "Time [s]" if not specified in the additional arguments
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = 'Time [s]'

        # set the y-axis label based on the kind and unit of the first data point if not specified in the additional
        # arguments and all sensor have the same kind and unit
        if 'ylabel' not in kwargs:
            try:
                first_kind = self[0].timeseries.sensor.kind
                first_unit = self[0].timeseries.sensor.unit
                equal = True
                for element in self[1:]:
                    if element.timeseries.sensor.kind != first_kind or element.timeseries.sensor.unit != first_unit:
                        equal = False
                        break

                if equal:
                    kwargs['ylabel'] = f'{first_kind.capitalize()} [{first_unit}]'
            except AttributeError:
                pass

        self.to_pandas().plot(**kwargs)
        if show:
            plt.show()

    def to_pandas(self):
        """
        Convert the data points list into a pandas DataFrame.

        Returns
        -------
        pandas.DataFrame
            The dataframe.
        """
        dfs = [dps.to_pandas() for dps in self]
        conc = pd.concat(dfs, axis="columns")
        return conc

    def create(self, **kwargs):
        print('## Datapoints are created through the Timeseries API / resource')
