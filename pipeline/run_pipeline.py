from modeltestSDK.client import SDKclient
from modeltestSDK.utils import get_datetime_date

from .add_sensors import add_sensors
from .add_campaign import fill_campaign


def main():
    client = SDKclient()
    campaign_dir = "C:/Users/jen/Documents/STT"
    campaign = client.campaign.create(name=campaign_dir.split("/")[-1],
                                      description="Modeltest for SWACH",
                                      date=get_datetime_date("180120120000"),
                                      location="STADT TOWING TANK",
                                      diameter=70,  # main hull cylinder
                                      scale_factor=75,  # står i rapporten
                                      water_density=1025,  # usikkert
                                      water_depth=300,  # står kun >300
                                      transient=3 * 60 * 60)  # 3 hours in seconds)
    add_sensors(campaign=campaign, client=client)
    concept_ids = ["M206", "M207"]
    fill_campaign(campaign, concept_ids, client, campaign_dir)


if __name__ == "__main__":
    main()
