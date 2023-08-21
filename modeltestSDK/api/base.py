from modeltestSDK.utils import format_class_name


class BaseAPI:
    """Base API with methods common for all APIs."""

    def __init__(self, client):
        self._resource_path: str = format_class_name(self.__class__.__name__)
        self.client = client

    def delete(self, item_id: str, secret_key: str = None):
        """
        Delete item by id

        Parameters
        ----------
        item_id : str
            Item identifier
        secret_key : str
            Secret key to allow deletion of read only items

        Notes
        -----
        Deleting items requires administrator privileges.
        """
        resp = self.client.delete(self._resource_path, endpoint=item_id, parameters=dict(secret_key=secret_key))
        return resp

    def update(self, item_id: str, body: dict, secret_key: str = None):
        """
        Update item by id

        Parameters
        ----------
        item_id : str
            Item identifier
        body : dict
            Request body
        secret_key : str
            Secret key to allow update of read only items
        """
        resp = self.client.patch(self._resource_path, endpoint=item_id, parameters=dict(secret_key=secret_key),
                                 body=body)
        return resp
