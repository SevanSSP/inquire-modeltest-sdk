import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union
from .utils import make_serializable, from_datetime_string
import datetime
class BaseResource(object):
    def __str__(self):
        return json.dumps(make_serializable(self.dump()), indent=2)

    def __repr__(self):
        return self.__str__()

    def dump(self):
         '''
         Dump the instance into a json serializable Python data type.

         Parameters
         ----------
         camel_case : bool, optional
             Use camelCase for attribute names. Defaults to False.

         Returns
         -------
         Dict[str, Any]
             A dictionary representation of the instance.
        '''
         d = {key: value for key, value in self.__dict__.items() if value is not None and not key.startswith("_")}
         return d

    def to_pandas(self, ignore: List[str]=None):
        """
        Convert the instance into a pandas DataFrame.

        Parameters
        ----------
        ignore : List[str]
            List of row keys to not include when converting to a data frame.

         Returns
         -------
        pandas.DataFrame
            The dataframe.
        """
        ignore = list() if ignore is None else ignore
        dumped = self.dump()

        df = pd.DataFrame(columns=["value"])
        for name, value in dumped.items():
            if name not in ignore:
                df.loc[name] = [value]
        return df

    def to_dict(self):
        return vars(self)

class ResourceList(BaseResource):
    resources = list()

    def __iter__(self):
        for r in self.resources:
            yield r

    def __len__(self):
        return len(self.resources)

    def dump(self):
        return [_.dump() for _ in self]

    def to_pandas(self, ignore: List[str]=None):
        return pd.DataFrame (self.dump())

class Campaign(BaseResource):

    def __init__(self, name: str, description: str, location: str, date: any, diameter: float,
               scale_factor: float, water_density: float, water_depth: float, transient: float, id: str = None, client=None, exists: bool = False):
        #if not isinstance(date, datetime.datetime):
        #    try:
        #        date = from_datetime_string(date)
        #    except ValueError:
        #        raise ValueError("Could not convert datetime string to datetime object")

        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.date = date
        self.diameter = diameter
        self.scale_factor = scale_factor
        self.water_density = water_density
        self.water_depth = water_depth
        self.transient = transient
        self._client = client
        print(self._client)

    def __str__(self):
        return f"<Campaign {self.name}>"

    @classmethod
    def get_existing(cls, name: str, client=None):
        content = client.campaign.get(client.campaign.get_id(name=name))

        return cls(name=content['name'], description=content['description'], location=content['location'],
            date=content['date'], diameter=content['diameter'], scale_factor=content['scale_factor'],
            water_density=content['water_density'], water_depth=content['water_depth'],
            transient=content['transient'], id=content['id'], client=client)

    def update(self):
        campaign_dict = self.to_dict().copy()
        campaign_dict.pop('_client', None)
        if not self.id:
            content = self._client.campaign.create(body=campaign_dict)
            print("CONTENT", content)
            if 'id' in content:
                self.id = content['id']
        else:
            print("PATCH", self._client.campaign.patch(body=campaign_dict, campaign_id=self.id))
