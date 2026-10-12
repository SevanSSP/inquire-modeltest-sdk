"""
Configurations
"""
from datetime import timedelta
from typing import Literal, Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class CacheConfig(BaseModel):
    cache_name: str = "mtdb"
    backend: Literal["sqlite"] = "sqlite"
    use_cache_dir: bool = True
    expire_after: timedelta = timedelta(days=7)


class Config(BaseSettings, env_prefix="INQUIRE_MODELTEST_"):
    """
    Client configuration, from arguments or INQUIRE_MODELTEST_* environment variables.

    Microsoft sign-in needs tenant_id, api_client_id (the model test API's app registration) and client_id: a
    public client for users signing in in the browser, or a service principal together with client_secret.
    """
    api_host: str
    tenant_id: Optional[str] = None
    api_client_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token_cache_path: Optional[str] = None
    base_url: str = "api"
    version: str = "v1"
    log_level: str = "info"
    cache_settings: CacheConfig = CacheConfig()
    requests_max_retries: int = 5
    requests_backoff_factor: float = 1.0
    request_timeout: float = 60.0
    token_expiry_margin: float = 60.0
