"""
Configurations
"""
import os


class Config:
    """
    Select between local host and azure
    """
    host = os.environ.get("INQUIRE_MODELTEST_API_HOST", "https://inquire-modeltest.azurewebsites.net")
    base_url = "api"
    version = 'v1'
