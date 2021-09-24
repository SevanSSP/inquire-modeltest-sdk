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


class LocalConfig(Config):
    """
    Local context configuration
    """
    host: str = os.environ.get("INQUIRE_MODELTEST_API_HOST", "http://localhost:8080/")
