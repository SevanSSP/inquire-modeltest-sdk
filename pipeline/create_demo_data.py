from modeltestSDK.resources import Campaign, Test
from modeltestSDK.client import SDKclient
import datetime


data = [
        dict(name="Electron GmbH2",
             description="Development of floating electrical substation for harsh environment.",
             date=datetime.datetime.utcnow(),
             location="Stadt",
             diameter=60,
             scale_factor=1,
             water_density=1025,
             water_depth=900,
             transient=200.),
        dict(name="Aladdin Oil2",
             description="Development of FPSO for arctic environment.",
             date=datetime.datetime.utcnow(),
             location="Sintef",
             diameter=40,
             scale_factor=1,
             water_density=1025,
             water_depth=950,
             transient=200.),
    ]


def demo_campaign(client):
    client.campaign.create(name="SWATCH",
             description="Development of floating electrical substation for harsh environment.",
             date=(datetime.datetime.utcnow()).isoformat(),
             location="Stadt",
             diameter=60,
             scale_factor=1,
             water_density=1025,
             water_depth=900,
             transient=200.2)
    client.campaign.create(name="Aladdin Oil2",
             description="Development of FPSO for arctic environment.",
             date=(datetime.datetime.utcnow()).isoformat(),
             location="Sintef",
             diameter=40,
             scale_factor=1,
             water_density=1025,
             water_depth=950,
             transient=200.)




if __name__ == "__main__":
    client = SDKclient()
    demo_campaign(client)

    camp_id = client.campaign.get_id("SWATCH")
    client.test.create(dict(description = "wavecalibration", test_date = (datetime.datetime.utcnow()).isoformat(), direction = "north", campaign_id = camp_id, type = "Floater"))
