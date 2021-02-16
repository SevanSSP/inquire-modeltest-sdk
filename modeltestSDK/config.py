"""
Configurations
"""
import os


class Config:
    """
    Client configuration
    """
    host: str = os.environ.get("INQUIRE_MODELTEST_API_HOST")
    base_url: str = "api"
    version: str = "v1"
    log_level: str = "info"


class LocalConfig(Config):
    """
    Local context configuration
    """
    host: str = os.environ.get("INQUIRE_MODELTEST_API_HOST", "http://localhost:8080/")
