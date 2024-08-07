from __future__ import annotations
import pandas as pd
from pydantic import BaseModel
from typing import List, Optional, Union, Any, TypeVar
from modeltestsdk.utils import make_serializable
import typing
import re


class Resource(BaseModel):
    client: Optional[Any] = None
    id: Optional[str] = None

    @staticmethod
    def _api_object_name(resource_name: str):
        return resource_name[0].lower() + re.sub('([A-Z]{1})', r'_\1', resource_name[1:]).lower()

    def _api_object(self):
        if hasattr(self.client, self._api_object_name(self.__class__.__name__)):
            return getattr(self.client, self._api_object_name(self.__class__.__name__))
        else:
            return None

    def create(self, read_only: bool = False, admin_key=None):
        if not self.id:
            try:
                if admin_key is None:
                    resource = self._api_object().create(
                        **make_serializable(self.model_dump(exclude={"client", 'id', 'datapoints_created_at', 'type'})),
                        read_only=read_only)
                else:
                    resource = self._api_object().create(
                        **make_serializable(self.model_dump(exclude={"client", 'id', 'datapoints_created_at', 'type'})),
                        read_only=read_only, admin_key=admin_key)
                self.id = resource.id
            except AttributeError as e:
                if self.client is None:
                    raise AttributeError('No client provided, unable to create object')
                else:
                    raise e  # pragma: no cover
        else:
            print(f"Resource {self.__class__.__name__} with id {self.id} already exists")

    def update(self, secret_key: str = None):
        self._api_object().update(item_id=self.id, body=make_serializable(self.model_dump(exclude={"client", 'id'})),
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
        See keyword arguments on pydantic.BaseModel.model_dump()
        """
        df = pd.DataFrame(columns=["value"])
        for name, value in self.model_dump().items():
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

    def append(self, item: ResourceType) -> None:
        """
        Appends an item to the list.

        Parameters:
            item (ResourceType): The item to append to the list.

        Returns:
            None

        Raises:
            TypeError: If the type of the item is not one of the expected types.
        """
        if not any(type(item).__name__ == t.__name__ for t in self._expected_types()):
            raise TypeError(f"Invalid type {type(item)} in {self.__class__.__name__}")

        super().append(item)

    def create(self, read_only: bool = False, admin_key: str = None) -> None:
        """
        Create the new objects in the database.

        Parameters:
            read_only (bool): If True, the object will be called with read_only set to True for each item.
            admin_key (str): An optional admin key to be passed to allow creation of certain objects.

        Returns:
            None
        """
        for item in self:
            item.create(read_only=read_only, admin_key=admin_key)

    def scalar(self):
        """
        Returns the scalar value of the object.

        This function checks the length of the object. If the length is equal to one, it returns the element itself.
        If the length is zero, it returns None. Otherwise, it raises a ValueError with the message
        'More than one resource found'.

        Returns:
            The scalar value of the object.

        Raises:
            ValueError: If the length of the object is greater than one.
        """
        if len(self) == 1:
            return self[0]
        elif len(self) == 0:
            return None
        else:
            raise ValueError('More than one resource found')

    def get_by_id(self, id) -> Union[ResourceType, None]:
        """
        Returns a resource from the collection based on its ID.

        Parameters:
            id (int): The ID of the resource to retrieve.

        Returns:
            Union[ResourceType, None]: The resource with the specified ID, or None if it does not exist.
        """
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
        See keyword arguments on pydantic.BaseModel.model_dump()
        """
        return pd.DataFrame([_.model_dump(exclude={"client"}, **kwargs) for _ in self])
