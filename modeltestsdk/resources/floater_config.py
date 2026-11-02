from typing import Optional
from .base import Resource, Resources


class FloaterConfig(Resource):
    id: Optional[str] = None
    name: str
    description: str
    campaign_id: str
    characteristic_length: float
    draft: float
    heading: Optional[float] = None  # degrees clockwise seen from above, from Sevan Global x to the LQ
    vcg: Optional[float] = None  # specified vertical centre of gravity above the keel (m)
    geometry: Optional[dict] = None  # the hull's shape: {"type": "circular" | "rectangular" | "sevancircular", ...}
    turn: Optional[float] = None  # the hull's turn from the campaign's LQ (degrees), set by the API

    def coordinates(self) -> dict:
        """The config's frames and every sensor's position and direction in Sevan Global (as the coordinate viewer)."""
        return self.client.floater_config.coordinates(self.id)


class FloaterConfigs(Resources[FloaterConfig]):
    pass
