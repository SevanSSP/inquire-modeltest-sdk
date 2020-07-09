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
    campaign_dir = "C:/Users/hly/Documents/STT"
    campaign = client.campaign.create(name=campaign_dir.split("/")[-1],
                                      description="Modeltest for SWACH",
                                      date=get_datetime_date("180120120000"),
                                      location="STADT TOWING TANK",
                                      diameter=70,  # main hull cylinder
                                      scale_factor=75,  # står i rapporten
                                      water_density=1025,  # usikkert
                                      water_depth=4.1 * 75,  # står kun >300
                                      transient=3 * 60 * 60)  # 3 hours in seconds)
    #add_sensors(campaign=campaign, client=client)

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
