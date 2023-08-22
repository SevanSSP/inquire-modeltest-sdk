from __future__ import annotations
import pandas as pd
from pydantic import BaseModel
from typing import List, Optional, Union, Any, TypeVar
from modeltestSDK.utils import make_serializable
import typing
import re


class Resource(BaseModel):
    client: Optional[Any]
    id: Optional[str]

    @staticmethod
    def _api_object_name(resource_name: str):
        return resource_name[0].lower() + re.sub('([A-Z]{1})', r'_\1', resource_name[1:]).lower()

    def _api_object(self):
        if hasattr(self.client, self._api_object_name(self.__class__.__name__)):
            return getattr(self.client, self._api_object_name(self.__class__.__name__))
        else:
            return None

    def create(self, admin_key=None):
        try:
            if admin_key is None:
                resource = self._api_object().create(
                    **make_serializable(self.dict(exclude={"client", 'id', 'datapoints_created_at', 'type'})))
            else:
                resource = self._api_object().create(
                    **make_serializable(self.dict(exclude={"client", 'id', 'datapoints_created_at', 'type'})),
                    admin_key=admin_key)
            self.id = resource.id
        except AttributeError as e:
            if self.client is None:
                raise AttributeError('No client provided, unable to create object')
            else:
                raise e  # pragma: no cover

    def update(self, secret_key: str = None):
        self._api_object().update(item_id=self.id, body=make_serializable(self.dict(exclude={"client", 'id'})),
                                  secret_key=secret_key)

    def delete(self, secret_key: str = None):
        self._api_object().delete(item_id=self.id, secret_key=secret_key)

    def to_pandas(self, **kwargs) -> pd.DataFrame:
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
        df = pd.DataFrame(columns=["value"])
        for name, value in self.dict().items():
            if name not in ("client",):
                df.loc[name] = [value]
        return df


ResourceType = TypeVar('ResourceType', bound=Resource)


class Resources(List[ResourceType]):
    def __init__(self, items: List[ResourceType] = None) -> None:
        if items:
            self._check_types(items)
            super().__init__(items)

    def filter(self, inplace: bool = False, **kwargs) -> Union[None, Resources]:
        """
        Filter resources based on keyword arguments.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments used for filtering.
        inplace : bool
            Flag to indicate if list should be filtered in-place or return new list


        Returns
        -------
            Filtered resources.
        """
        filtered_resources = [resource for resource in self if
                              all(getattr(resource, attr) == value for attr, value in kwargs.items())]
        if inplace:
            self.clear()
            self.extend(filtered_resources)
        else:
            return type(self)(filtered_resources)

    def _expected_types(self):
        return self.__orig_bases__[0].__args__[0].__args__ \
            if isinstance(self.__orig_bases__[0].__args__[0], typing._UnionGenericAlias) \
            else [self.__orig_bases__[0].__args__[0]]

    def _check_types(self, items: List[Resource]) -> None:
        for item in items:
            if not any(type(item).__name__ == t.__name__ for t in self._expected_types()):
                raise TypeError(f"Invalid type {type(item)} in {self.__class__.__name__}")

    def append(self, item: ResourceType, admin_key: str = None) -> None:
        if not any(type(item).__name__ == t.__name__ for t in self._expected_types()):
            raise TypeError(f"Invalid type {type(item)} in {self.__class__.__name__}")
        if item.id or item.__class__.__name__ == 'DataPoints':
            super().append(item)
        else:
            item.create(admin_key=admin_key)
            super().append(item)

    def get_by_id(self, id) -> Union[ResourceType, None]:
        for i in self:
            if i.id == id:
                return i
        return None

    def to_pandas(self, **kwargs) -> pd.DataFrame:
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
        return pd.DataFrame([_.dict(exclude={"client"}, **kwargs) for _ in self])
