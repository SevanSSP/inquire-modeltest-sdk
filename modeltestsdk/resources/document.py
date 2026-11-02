from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CampaignDocument(BaseModel):
    """A document of a campaign (report, test programme, drawing), kept in Blob storage by class."""
    path: str  # in the campaign's folder, e.g. "Main report/report.pdf"
    name: str  # the path without the class folder
    document_class: str
    size_bytes: int
    modified: Optional[datetime] = None
