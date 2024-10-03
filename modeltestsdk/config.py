"""
Configurations
"""
import os
from datetime import timedelta, datetime
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class CacheConfig(BaseModel):
    cache_name: str = "mtdb"
    backend: Literal["sqlite"] = "sqlite"
    use_cache_dir: bool = True
    expire_after: datetime = timedelta(days=7)


class Config(BaseSettings, env_prefix="INQUIRE_MODELTEST_"):
    """
    Client configuration
    """
    api_host: str
    api_user: str
    api_password: str
    base_url: str = "api"
    version: str = "v1"
    log_level: str = "info"
    cache_settings: CacheConfig = CacheConfig()
    requests_max_retries: int = 5
    requests_backoff_factor: float = 1.0
