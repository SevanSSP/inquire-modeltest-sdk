from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date

from .add_sensors import add_sensors, sensorDict
from .add_campaign import fill_campaign

import time


def main():

    ans = input("You are about to run the pipeline for the STT SWACH model test.\nIf this is already imported you "
          "will experience issues with data duplicates.\nAre you sure you want to import? [y/N] ")

    if ans != "y":
        return

    tic = time.perf_counter()

    client = SDKclient()

    # Specify path to folder where campaign is locally stored
    campaign_dir = "C:/Users/nbu/Documents/STT"

    # Create initial campaign in database
    campaign = client.campaign.create(name="STT",
                                      description="Modeltest for SWACH and HE Modu",
                                      date=get_datetime_date("180120120000"),
                                      location="STADT TOWING TANK",
                                      waterline_diameter=70,    # Main hull cylinder
                                      scale_factor=75,          # From the report
                                      water_density=1025,       # Not sure if this is correct
                                      water_depth=4.1 * 75,     # Source for water depth being 4.1m is fisk.no, could not find any other official number
                                      transient=3 * 60 * 60)    # 3 hours in seconds

    # Add all the sensors that were used in STT campaign
    add_sensors(campaign=campaign, client=client)

    concept_ids = ["M206", "M207"]
    fill_campaign(campaign, concept_ids, client, campaign_dir)

    toc = time.perf_counter()
    print(f"Importing campaign took {toc - tic:0.4f} seconds")

    # Set default return value for sensor Dictionary
    all_sensors = client.sensor.get_all()
    for sensor in all_sensors:
        sensorDict.setdefault(sensor.name, sensor.name)


if __name__ == "__main__":
    main()
