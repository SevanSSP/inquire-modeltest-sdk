from modeltestSDK.client import Client
from pipeline.WhitePearl.add_sensor import add_sensors
from pipeline.WhitePearl.add_floater_config import add_floater_configs
from pipeline.WhitePearl.add_tests import add_tests
import datetime

import time


def main():

    ans = input("You are about to run the pipeline for the White pearl model test.\nIf this is already imported you "
          "will experience issues with data duplicates.\nAre you sure you want to import? [y/N] ")

    if ans != "y":
        return

    tic = time.perf_counter()

    # Specify path to folder where campaign is locally stored
    # campaign_dir = "C:/Users/jen.SEVAN/Documents/505 Stockman FPU_2008"
    campaign_dir = r"C:/Users/ebg/Documents/White_Pearl_MT/505 Stockman FPU_2008"

    client = Client()
    # Create initial campaign in database
    campaign = client.campaign.create(name="White Pearl",
                                      description="Sevan ICE-FPU. Ice breaking hull", #Todo: update
                                      date=datetime.datetime(year=2008, month=2, day=1).isoformat(),
                                      location="MARINTEK",
                                      scale_factor=62.14,          # From the report
                                      water_depth=290,
                                      read_only=True)

    # Add all the sensors that were used in STT campaign
    add_sensors(campaign=campaign, client=client)
    add_floater_configs(campaign=campaign, client=client)

    add_tests(campaign_dir=campaign_dir, campaign=campaign, client=client)

    toc = time.perf_counter()
    print(f"Importing campaign took {toc - tic:0.4f} seconds")


if __name__ == "__main__":
    main()
