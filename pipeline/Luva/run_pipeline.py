from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date
from pipeline.Luva.add_floater_config import add_floater_configs
from pipeline.Luva.add_sensor import add_sensors
from pipeline.Luva.add_test import add_tests
import datetime

import time


def main():

    ans = input("You are about to run the pipeline for the Luva model test.\nIf this is already imported you "
          "will experience issues with data duplicates.\nAre you sure you want to import? [y/N] ")

    if ans != "y":
        return

    tic = time.perf_counter()

    # Specify path to folder where campaign is locally stored
    campaign_dir = "C:/Users/jen.SEVAN/Documents/529 Luva_2009"
    #campaign_dir = r"C:/Users/ebg/Documents/White_Pearl_MT/505 Stockman FPU_2008"

    client = SDKclient()
    # Create initial campaign in database
    campaign = client.campaign.create(name="Luva",
                                      description="SEVAN LUVA FSU, a mono-column structure to be permanently moored "
                                                  "at the Luva Field",
                                      date=datetime.datetime(year=2010, month=7, day=20).isoformat(),
                                      location="MARINTEK",
                                      scale_factor=70,          # From the report
                                      water_depth=350,
                                      read_only=True)

    add_sensors(campaign=campaign, client=client)

    add_floater_configs(campaign=campaign, client=client)

    add_tests(campaign_dir=campaign_dir, campaign=campaign, client=client)

    toc = time.perf_counter()
    print(f"Importing campaign took {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    main()
