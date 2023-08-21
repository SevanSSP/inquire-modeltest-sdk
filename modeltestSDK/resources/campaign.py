from typing import Optional
from datetime import datetime
from .base import Resource, Resources
from .sensor import Sensors
from .test import Tests
from floater_config import FloaterConfigs


class Campaign(Resource):
    name: str
    description: str
    location: str
    date: datetime
    scale_factor: float
    water_depth: float
    read_only: Optional[bool] = False

    def sensors(self, limit: int = 100, skip: int = 0) -> Sensors:
        """Fetch sensors."""
        return self.client.sensor.get_by_campaign_id(self.id, limit=limit, skip=skip)

    def tests(self, limit: int = 100, skip: int = 0) -> Tests:
        """Fetch tests."""
        return self.client.test.get_by_campaign_id(self.id, limit=limit, skip=skip)

    def floater_configurations(self, limit: int = 100, skip: int = 0) -> FloaterConfigs:
        """Fetch floater configurations."""
        return self.client.floaterconfig.get_by_campaign_id(self.id, limit=limit, skip=skip)


class Campaigns(Resources[Campaign]):
    pass
