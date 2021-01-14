from modeltestSDK.resources import Campaign, Sensor
from modeltestSDK.client import SDKclient

restrict_access = True

position1 = {'x': 310.70,'y':0,'z':0}
position2 = {'x': 0,'y':0,'z':0}
position3 = {'x': 0,'y':-310.70,'z':0}

positionBOW = {'x': 57.50,'y':12.50,'z':0}
positionWL = {'x': 0,'y':0,'z':0}
positionTOPDKC = {'x': 0,'y':0,'z':-39.10}

def add_sensors(campaign: Campaign, client: SDKclient):

    client.sensor.create(name="WAVE_1",
                     description="Wave elevation at position 1, measured during test",
                     unit="m",
                     kind="length",
                     x=position1.x,
                     y=position1.y,
                     z=position1.z,
                     is_local=False,
                     fs=1/200,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="WAVE_3",
                     description="Wave elevation at position 3, measured during test",
                     unit="m",
                     kind="length",
                     x=position3.x,
                     y=position3.y,
                     z=position3.z,
                     is_local=False,
                     fs=1/200,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="RELW_01",
                     description="Wave elevation at bow of FPSO",
                     unit="m",
                     kind="length",
                     x=positionBOW.x,
                     y=positionBOW.y,
                     z=positionBOW.z,
                     is_local=True,
                     fs=1/200,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="WAVE_1_CAL",
                     description="Calibrated wave at position 2",
                     unit="m",
                     kind="length",
                     x=position1.x,
                     y=position1.y,
                     z=position1.z,
                     is_local=False,
                     fs=1/200,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="WAVE_2_CAL",
                     description="Calibrated wave at position 2",
                     unit="m",
                     kind="length",
                     x=position2.x,
                     y=position2.y,
                     z=position2.z,
                     is_local=False,
                     fs=1/200,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)


    client.sensor.create(name="WAVE_3_CAL",
                     description="Calibrated wave at position 3",
                     unit="m",
                     kind="length",
                     x=position3.x,
                     y=position3.y,
                     z=position3.z,
                     is_local=False,
                     fs=1/200,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="XPOS_TOPDKC",
                     description="Displacement of TOP DECK in x-direction",
                     unit="m",
                     kind="length",
                     x=positionTOPDKC.x,
                     y=positionTOPDKC.y,
                     z=positionTOPDKC.z,
                     is_local=False,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="YPOS_TOPDKC",
                     description="Displacement of TOP DECK in y-direction",
                     unit="m",
                     kind="length",
                     x=positionTOPDKC.x,
                     y=positionTOPDKC.y,
                     z=positionTOPDKC.z,
                     is_local=False,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="ZPOS_TOPDKC",
                     description="Displacement of TOP DECK in z-direction",
                     unit="m",
                     kind="length",
                     x=positionTOPDKC.x,
                     y=positionTOPDKC.y,
                     z=positionTOPDKC.z,
                     is_local=False,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="ROLL",
                     description="Rotation of FPSO about x-axis",
                     unit="deg",
                     kind="angle",
                     x=0,
                     y=0,
                     z=0,
                     is_local=True,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="PITCH",
                     description="Rotation of FPSO about y-axis",
                     unit="deg",
                     kind="angle",
                     x=0,
                     y=0,
                     z=0,
                     is_local=True,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

     client.sensor.create(name="YAW",
                     description="Rotation of FPSO about z-axis",
                     unit="deg",
                     kind="angle",
                     x=0,
                     y=0,
                     z=0,
                     is_local=True,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="XPOS_WL",
                     description="Displacement of FPSO at WL in x-direction",
                     unit="m",
                     kind="length",
                     x=0,
                     y=0,
                     z=0,
                     is_local=False,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="YPOS_WL",
                     description="Displacement of FPSO at WL in y-direction",
                     unit="m",
                     kind="length",
                     x=0,
                     y=0,
                     z=0,
                     is_local=False,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)

    client.sensor.create(name="ZPOS_WL",
                     description="Displacement of FPSO at WL in z-direction",
                     unit="m",
                     kind="length",
                     x=0,
                     y=0,
                     z=0,
                     is_local=False,
                     fs=1/20,
                     intermittent=False,
                     campaign_id=campaign.id,
                     read_only=restrict_access)
