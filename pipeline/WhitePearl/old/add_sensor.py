from modeltestSDK import Client
from modeltestSDK.resources import Campaign

restrict_access = True

position1 = {'x': 310.70, 'y': 0, 'z': 0}
position2 = {'x': 0, 'y': 0, 'z': 0}
position3 = {'x': 0, 'y': -310.70, 'z': 0}

positionBOW = {'x': 57.50, 'y': 12.50, 'z': 0}
positionWL = {'x': 0, 'y': 0, 'z': 0}
positionTOPDKC = {'x': 0, 'y': 0, 'z': -39.10}


def add_sensors(campaign: Campaign, client: Client):
    sensor = client.sensor.create(name="WAVE_1",
                                  description="Wave elevation at position 1, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="comment",
                      comment='denoted "_CAL" in wave calibration tests',
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="WAVE_2",
                                  description="Wave elevation at position 2, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position2['x'],
                                  y=position2['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="reference signal",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="WAVE_3",
                                  description="Wave elevation at position 3, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position3['x'],
                                  y=position3['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="comment",
                      comment='denoted "_CAL" in wave calibration tests',
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="RELW_01",
                                  description="Relative wave elevation at bow of FPSO, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=positionBOW['x'],
                                  y=positionBOW['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    #  This is the WAVE_1 sensor in the calibration tests
    # client.sensor.create(name="WAVE_1_CAL",
    #                  description="Calibrated wave at position 2",
    #                  unit="m",
    #                  kind="length",
    #                  x=position1['x'],
    #                  y=position1['y'],
    #                  z=position1['z'],
    #                  is_local=False,
    #                  campaign_id=campaign.id,
    #                  read_only=restrict_access)

    #  This is the WAVE_1 sensor in the calibration tests
    # client.sensor.create(name="WAVE_3_CAL",
    #                  description="Calibrated wave at position 3",
    #                  unit="m",
    #                  kind="length",
    #                  x=position3['x'],
    #                  y=position3['y'],
    #                  z=position3['z'],
    #                  is_local=False,
    #                  campaign_id=campaign.id,
    #                  read_only=restrict_access)

    sensor = client.sensor.create(name="XPOS_TOPDKC",
                                  description="Displacement of TOP DECK in basin/Sevan x-direction",
                                  unit="m",
                                  kind="length",
                                  x=positionTOPDKC['x'],
                                  y=positionTOPDKC['y'],
                                  z=positionTOPDKC['z'],
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="YPOS_TOPDKC",
                                  description="Displacement of TOP DECK in basin y-direction",
                                  unit="m",
                                  kind="length",
                                  x=positionTOPDKC['x'],
                                  y=positionTOPDKC['y'],
                                  z=positionTOPDKC['z'],
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_TOPDKC",
                                  description="Displacement of TOP DECK in basin z-direction",
                                  unit="m",
                                  kind="length",
                                  x=positionTOPDKC['x'],
                                  y=positionTOPDKC['y'],
                                  z=positionTOPDKC['z'],
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="ROLL",
                                  description="Rotation of FPSO about basin/Sevan x-axis",
                                  unit="deg",
                                  kind="angle",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="roll",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="PITCH",
                                  description="Rotation of FPSO about basin y-axis",
                                  unit="deg",
                                  kind="angle",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="YAW",
                                  description="Rotation of FPSO about basin z-axis",
                                  unit="deg",
                                  kind="angle",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="XPOS_WL",
                                  description="Displacement of FPSO at waterline in basin/Sevan x-direction",
                                  unit="m",
                                  kind="length",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="surge",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="YPOS_WL",
                                  description="Displacement of FPSO at waterline in basin y-direction",
                                  unit="m",
                                  kind="length",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_WL",
                                  description="Displacement of FPSO at waterline in basin z-direction",
                                  unit="m",
                                  kind="length",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: direct measurement",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
    
    client.tag.create(name="coordinate system: basin",
                      comment="right-hand coordinate system with x towards wave and z downwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    # ## Derived Sensors

    sensor = client.sensor.create(name="WAVE_3_Sevan",
                                  description="Wave elevation at position 3, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position3['x'],
                                  y=-position3['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="comment",
                      comment='denoted "_CAL" in wave calibration tests',
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="RELW_01_Sevan",
                                  description="Relative wave elevation at bow of FPSO, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=positionBOW['x'],
                                  y=-positionBOW['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="YPOS_TOPDKC_Sevan",
                                  description="Displacement of TOP DECK in Sevan y-direction",
                                  unit="m",
                                  kind="length",
                                  x=positionTOPDKC['x'],
                                  y=-positionTOPDKC['y'],
                                  z=-positionTOPDKC['z'],
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_TOPDKC_Sevan",
                                  description="Displacement of TOP DECK in Sevan z-direction",
                                  unit="m",
                                  kind="length",
                                  x=positionTOPDKC['x'],
                                  y=-positionTOPDKC['y'],
                                  z=-positionTOPDKC['z'],
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="PITCH_Sevan",
                                  description="Rotation of FPSO about Sevan y-axis",
                                  unit="deg",
                                  kind="angle",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="pitch",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="YAW_Sevan",
                                  description="Rotation of FPSO about Sevan z-axis",
                                  unit="deg",
                                  kind="angle",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="yaw",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="YPOS_WL_Sevan",
                                  description="Displacement of FPSO at waterline in Sevan y-direction",
                                  unit="m",
                                  kind="length",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="sway",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_WL_Sevan",
                                  description="Displacement of FPSO at waterline in Sevan z-direction",
                                  unit="m",
                                  kind="length",
                                  x=0,
                                  y=0,
                                  z=0,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    client.tag.create(name="source: in-house derived",
                      comment="",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="coordinate system: Sevan",
                      comment="right-hand coordinate system with x towards wave and z upwards",
                      sensor_id=sensor.id,
                      read_only=restrict_access)

    client.tag.create(name="heave",
                      sensor_id=sensor.id,
                      read_only=restrict_access)
