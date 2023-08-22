"""
Configurations
"""
import os
from datetime import timedelta


class Config:
    """
    Client configuration
    """
    host: str = os.environ.get("INQUIRE_MODELTEST_API_HOST")
    base_url: str = "api"
    version: str = "v1"
    log_level: str = "info"
    cache_settings = {'cache_name': 'mtdb',
                      'backend': 'sqlite',
                      'use_cache_dir': True,
                      'expire_after': timedelta(days=7)}
    requests_max_retries = 5
    requests_backoff_factor = 1.0
