from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union
from .base import Resource, Resources
from .document import CampaignDocument
from .floater_config import FloaterConfigs
from .sensor import Sensors
from .test import Tests


class Campaign(Resource):
    name: str
    description: str
    location: str
    date: datetime
    scale_factor: float
    water_depth: float
    main_characteristic_length: Optional[float] = None
    data_format: Optional[str] = None
    source_workbook: Optional[str] = None
    notes: Optional[str] = None
    # coordinate definitions (the lab's axes as signed Sevan axes, e.g. '+x', '-y'; angles in degrees)
    lab_axis_x: Optional[str] = None
    lab_axis_y: Optional[str] = None
    lab_axis_z: Optional[str] = None
    lab_local_axis_x: Optional[str] = None
    lab_local_axis_y: Optional[str] = None
    lab_local_axis_z: Optional[str] = None
    lab_local_offset: Optional[float] = None
    lab_local_origin_x: Optional[float] = None
    lab_local_origin_y: Optional[float] = None
    lab_local_origin_z: Optional[float] = None
    lab_global_turns: Optional[bool] = None
    lab_local_turns: Optional[bool] = None
    lq: Optional[float] = None
    north: Optional[float] = None
    north_type: Optional[str] = None
    z_origin: Optional[str] = None
    z_origin_config_id: Optional[str] = None
    baseline_above_keel: Optional[float] = None

    def sensors(self, limit: int = 100, skip: int = 0) -> Sensors:
        """Fetch sensors."""
        return self.client.sensor.get_by_campaign_id(self.id, limit=limit, skip=skip)

    def tests(self, limit: int = 100, skip: int = 0) -> Tests:
        """Fetch tests."""
        return self.client.test.get_by_campaign_id(self.id, limit=limit, skip=skip)

    def floater_configurations(self, limit: int = 100, skip: int = 0) -> FloaterConfigs:
        """Fetch floater configurations."""
        return self.client.floater_config.get_by_campaign_id(self.id, limit=limit, skip=skip)

    def documents(self) -> List[CampaignDocument]:
        """The campaign's documents (reports, test programmes, drawings)."""
        return self.client.campaign.documents(self.id)

    def download_document(self, path: str, destination: Union[str, Path] = ".") -> Path:
        """Downloads a document (its path as in documents()) into a folder, or to a file path. Returns the file."""
        return self.client.campaign.download_document(self.id, path, destination)


class Campaigns(Resources[Campaign]):
    pass
