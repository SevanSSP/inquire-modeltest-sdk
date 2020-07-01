from modeltestSDK.resources import Campaign, Sensor
from modeltestSDK.client import SDKclient

class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2


sensorDict = TwoWayDict()
sensorDict["Wave 1 Moonpool Slot 7 AI0-AI8"] = "wave2"


def add_sensors(campaign: Campaign, client: SDKclient):
    client.sensor.create(name="M206_COG X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M206_COG Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M206_COG Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COG Yaw",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COG Pitch",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COG Roll",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Yaw",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Pitch",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Roll",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M206_COF Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M206_COF Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Yaw",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Pitch",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Roll",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)


    # TODO: Oppdatere faktiske data, alt over her er ikke ekte data

    client.sensor.create(name='Wave 1 Moonpool Slot 7 AI0-AI8',
                         description='Wave model moonpool - A',
                         unit='mm',
                         kind='length',
                         x=-117,  # x, y, z alle i mm og modellskala
                         y=0,
                         z=(47.5 * 1000) / 75,
                         # 47.5 er høyden til dech på fullskala, i meter
                         is_local=True,  # usikker
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave 2 Front Model Slot 7 AI1-AI9',
                         description='Wave model front - B',
                         unit='mm',
                         kind='length',
                         x=755,
                         y=0,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave 3 Front Slot 7 AI2-AI10',
                         description='Wave front - C',
                         unit='mm',
                         kind='length',
                         x=1925,
                         y=370,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave 4 Side SLot 7 AI4-AI12',
                         description='Wave side - D',
                         unit='mm',
                         kind='length',
                         x=1095,
                         y=-2740,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave US Front Slot 7 AI3-AI11',
                         description='Wave side US - F',
                         unit='mm',
                         kind='length',
                         x=1925,
                         y=610,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='F_BB_Front_Slot 8 AI5',
                         description='Force BB Front',
                         unit='N',
                         kind='force',
                         x=4000,
                         y=-4000,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='F_SB_Front_Slot 8 AI6',
                         description='Force SB Front',
                         unit='N',
                         kind='force',
                         x=4000,
                         y=3800,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='F_BB_Aft_Slot 8 AI 4',
                         description='Force BB Aft',
                         unit='N',
                         kind='force',
                         x=-4600,
                         y=-4000,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='F_SB_Aft_Slot 8 AI3',
                         description='Force SB Aft',
                         unit='N',
                         kind='force',
                         x=-4600,
                         y=3800,
                         z=(47.5 * 1000) / 75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI aks, X, Y, Z',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=372.5,
                         z=(47.5 * 1000) / 75 + 60,
                         is_local=True,
                         campaign_id=campaign.id)

