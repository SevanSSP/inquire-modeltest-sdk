import os

os.environ["INQUIRE_MODELTEST_API_USER"] = "ebg"
os.environ["INQUIRE_MODELTEST_API_PASSWORD"] = "pass"
os.environ["INQUIRE_MODELTEST_API_HOST"] = r"http://127.0.0.1:8000"

from modeltestSDK import Client
from pipeline.utils import import_based_on_xls

client = Client()

xls_loc = "Pipeline_Input_White_Pearl.xls"
data_folder = r"C:\MTDBimport\WhitePearl"

import_based_on_xls(client=client, xls_loc=xls_loc, data_folder=data_folder)
