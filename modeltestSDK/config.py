"""
Configurations
"""
import os


class Config:
    """
    Select between local host and azure
    """
    host = os.environ.get("INQUIRE_MODELTEST_API_HOST", "inquire-modeltest-eqn.azurewebsites.net")
    base_url = "api"
    version = 'v1'
    log_level = 'info'
