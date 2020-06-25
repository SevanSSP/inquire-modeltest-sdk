import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Union
from .utils import make_serializable, from_datetime_string

class BaseResource:
    def __str__(self):
        return json.dumps(make_serializable(self.dump()), indent=2)

    def __repr__(self):
        return self.__str__()

    def dump(self):
         """
         Dump the instance into a json serializable Python data type.

         Parameters
         ----------
         camel_case : bool, optional
             Use camelCase for attribute names. Defaults to False.

         Returns
         -------
         Dict[str, Any]
             A dictionary representation of the instance.
         """
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





