from typing import Optional
from .base import Resource, Resources
from .tag import Tags
from .timeseries import TimeseriesList


class Sensor(Resource):
    id: Optional[str] = None
    campaign_id: str
    name: str
    description: str
    unit: str
    kind: str
    source: str
    x: float
    y: float
    z: Optional[float] = None
    position_reference: str
    position_heading_lock: bool
    position_draft_lock: bool
    positive_direction_definition: str
    area: Optional[float] = None

    def tags(self, limit: int = 100, skip: int = 100) -> Tags:
        """Retrieve tags on sensor."""
        return self.client.tag.get_by_sensor_id(self.id, limit=limit, skip=skip)

    def timeseries(self, limit: int = 100, skip: int = 100) -> TimeseriesList:
        """Retrieve time series on sensor."""
        return self.client.timeseries.get_by_sensor_id(self.id, limit=limit, skip=skip)


class Sensors(Resources[Sensor]):
    def print_full(self):  # pragma: no cover
        for i in self:
            print(f'{i.to_pandas()}\n')

    def print_small(self):  # pragma: no cover
        for i in self:
            print(f"{i.to_pandas().loc[['name', 'id', 'campaign_id', 'description']]}\n")

    def print_list(self):  # pragma: no cover
        print(f'id\tkind\tunit\tdescription')
        for i in self:
            print(f'{i.id}\t{i.kind}\t{i.unit}\t{i.description}')
