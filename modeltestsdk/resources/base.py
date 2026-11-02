from __future__ import annotations
import pandas as pd
from pydantic import BaseModel, RootModel, Field, PrivateAttr
from typing import List, Optional, Union, Any, TypeVar
from modeltestsdk.utils import make_serializable
import re


# Fields the API sets itself, never sent when creating or updating a resource
SERVER_FIELDS = {"client", "id", "type", "read_only", "datapoints_created_at", "n_points", "t_first", "t_last", "turn"}


class Resource(BaseModel):
    client: Optional[Any] = None
    id: Optional[str] = None
    read_only: Optional[bool] = None
    _upsert_status: Optional[str] = PrivateAttr(default=None)

    @property
    def upsert_status(self) -> Optional[str]:
        """'created', 'updated' or 'unchanged' if the resource comes from an upsert, otherwise None."""
        return self._upsert_status

    @staticmethod
    def _api_object_name(resource_name: str):
        return resource_name[0].lower() + re.sub('([A-Z]{1})', r'_\1', resource_name[1:]).lower()

    def _api_object(self):
        if hasattr(self.client, self._api_object_name(self.__class__.__name__)):
            return getattr(self.client, self._api_object_name(self.__class__.__name__))
        else:
            return None

    def create(self, read_only: bool = False):
        """Creates the resource in the API and sets its id. Creating a campaign needs the Admin role."""
        if not self.id:
            if self.client is None:
                raise AttributeError('No client provided, unable to create object')
            fields = make_serializable(self.model_dump(exclude=SERVER_FIELDS))
            resource = self._api_object().create(**fields, read_only=read_only)
            self.id = resource.id
            self.read_only = resource.read_only
        else:
            print(f"Resource {self.__class__.__name__} with id {self.id} already exists")

    def update(self):
        """Sends the resource's fields to the API."""
        self._api_object().update(item_id=self.id, body=make_serializable(self.model_dump(exclude=SERVER_FIELDS)))

    def delete(self):
        """Deletes the resource in the API."""
        self._api_object().delete(item_id=self.id)

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


class Resources(RootModel[List[ResourceType]]):
    root: List[ResourceType] = Field(default_factory=list)

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
        filtered_resources = [resource for resource in self.root if
                              all(getattr(resource, attr) == value for attr, value in kwargs.items())]
        if inplace:
            self.root.clear()
            self.root.extend(filtered_resources)
        else:
            return type(self)(filtered_resources)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item) -> ResourceType:
        return self.root[item]

    def __len__(self) -> int:
        return len(self.root)

    def append(self, item: ResourceType) -> None:
        new_list = self.root + [item]
        super().__init__(new_list)

    def extend(self, items: List[ResourceType]) -> None:
        new_list = self.root + [items]
        super().__init__(new_list)

    def create(self, read_only: bool = False) -> None:
        """
        Create the new objects in the database.

        Parameters:
            read_only (bool): If True, the object will be called with read_only set to True for each item.

        Returns:
            None
        """
        for item in self.root:
            item.create(read_only=read_only)

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
        if len(self.root) == 1:
            return self.root[0]
        elif len(self.root) == 0:
            return None
        else:
            raise ValueError('More than one resource found')

    def get_by_id(self, id: str) -> Union[ResourceType, None]:
        """
        Returns a resource from the collection based on its ID.

        Parameters:
            id (str): The ID of the resource to retrieve.

        Returns:
            Union[ResourceType, None]: The resource with the specified ID, or None if it does not exist.
        """
        for i in self.root:
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
        return pd.DataFrame([_.model_dump(exclude={"client"}, **kwargs) for _ in self.root])
