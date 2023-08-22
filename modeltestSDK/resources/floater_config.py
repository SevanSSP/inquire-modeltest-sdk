from typing import Optional
from .base import Resource, Resources


class FloaterConfig(Resource):
    id: Optional[str]
    name: str
    description: str
    campaign_id: str
    characteristic_length: float
    draft: float


class FloaterConfigs(Resources[FloaterConfig]):
    pass
