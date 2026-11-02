from typing import Iterable, List

from pydantic import BaseModel

from modeltestsdk.resources.base import Resource
from modeltestsdk.utils import format_class_name, to_jsonable

# Fields of a resource that are never sent in an upsert
NOT_UPSERTED = {"client", "id", "datapoints_created_at"}


def upsert_body(item) -> dict:
    """
    Body of one upsert item: a dict as is, or the fields set on a resource or pydantic model.
    Fields not sent are left as they are by the API; None clears a field.
    """
    if isinstance(item, Resource):
        body = item.model_dump(exclude=NOT_UPSERTED, exclude_unset=True)
    elif isinstance(item, BaseModel):
        body = item.model_dump(exclude_unset=True)
    else:
        body = dict(item)
    return to_jsonable(body)


class BaseAPI:
    """Base API with methods common for all APIs."""

    def __init__(self, client):
        self._resource_path: str = format_class_name(self.__class__.__name__)
        self.client = client

    def _upserted(self, data: dict, resource_class):
        """Resource from an upsert response item, with its upsert status."""
        obj = resource_class(**data, client=self.client)
        obj._upsert_status = data.get("status")
        return obj

    def _upsert_many(self, resource: str, endpoint: str, items: Iterable, resource_class, body=upsert_body) -> List:
        """PUTs a batch of items and returns the resources in request order. Nothing is stored if one item fails."""
        data = self.client.put(resource, endpoint, body=[body(item) for item in items])
        return [self._upserted(i, resource_class) for i in data]

    def delete(self, item_id: str):
        """
        Delete item by id

        Parameters
        ----------
        item_id : str
            Item identifier

        Notes
        -----
        Deleting needs write access to the campaign; read-only items and campaigns need the Admin role.
        """
        return self.client.delete(self._resource_path, endpoint=item_id)

    def update(self, item_id: str, body: dict):
        """
        Update item by id

        Parameters
        ----------
        item_id : str
            Item identifier
        body : dict
            Fields to change

        Notes
        -----
        Updating needs write access to the campaign; read-only items need the Admin role.
        """
        return self.client.patch(self._resource_path, endpoint=item_id, body=body)
