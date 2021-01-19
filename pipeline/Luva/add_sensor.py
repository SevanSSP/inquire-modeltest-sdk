from modeltestSDK import SDKclient, Campaign

restrict_access = True

position1 = {'x': 310.70, 'y': 0, 'z': 0}
position2 = {'x': 0, 'y': 0, 'z': 0}
position3 = {'x': 0, 'y': -310.70, 'z': 0}

positionBOW = {'x': 17.5, 'y': -30, 'z': -72}
positionWL = {'x': 0, 'y': 0, 'z': -30}


pos_BL = {'x': 0, 'y': 0, 'z': 0}

 #TODO: Add tags, update desc, update coords

def add_sensors(campaign: Campaign, client: SDKclient):
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

    sensor = client.sensor.create(name="WAVE_3",
                                  description="Wave elevation at position 3, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="CURRENT_2",
                                  description="Current speed at position 2, zero at SWL - positive upwards",
                                  unit="m/s",
                                  kind="velocity",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="WIND",
                                  description="Wind speed. Derived quasi speed",
                                  unit="m/s",
                                  kind="velocity",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="REL_WAVE_0",
                                  description="Wave elevation at position 1, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="REL_WAVE_120",
                                  description="Wave elevation at position 1, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="REL_WAVE_270",
                                  description="Wave elevation at position 1, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="REL_WAVE_300",
                                  description="Wave elevation at position 1, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="REL_WAVE_MOONP_CENTRE",
                                  description="Relative wave elevation at center of moonpool",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="REL_WAVE_MOONP_120",
                                  description="Relative wave elevation at center of moonpool",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="REL_WAVE_MOONP_300",
                                  description="Relative wave elevation at center of moonpool",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="GREEN_WATER_300_1",
                                  description="Green water on process deck. Dir 300 deg",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="GREEN_WATER_300_2",
                                  description="Green water on process deck. Dir 300 deg",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="GREEN_WATER_300_3",
                                  description="Green water on process deck. Dir 300 deg",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="X_ACC_MOONP_C",
                                  description="Near centre, EL 65m",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Y_ACC_MOONP_C",
                                  description="Near centre, EL 65m",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Z_ACC_MOONP_C",
                                  description="Near centre, EL 65m",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="X_ACC_PDK_120",
                                  description="Near centre, EL 48m",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Y_ACC_PDK_120",
                                  description="Near centre, EL 48m",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Z_ACC_PDK_120",
                                  description="Near centre, EL 48m",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="FZ_PONTOON",
                                  description="External force downwards, Section of pontoon, b=4.6m",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="M_300_PONTOON",
                                  description="External force downwards, Section of pontoon, b=4.6m",
                                  unit="kNm",
                                  kind="force", #TODO: Sensor type
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="PRESSURE_TOP",
                                  description="",
                                  unit="Pa",
                                  kind="pressure",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="PRESSURE_BOTTOM",
                                  description="",
                                  unit="Pa",
                                  kind="pressure",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="TENSION_L01",
                                  description="Mooring line tensions at fairlead",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="TENSION_L02",
                                  description="Mooring line tensions at fairlead",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="TENSION_L05",
                                  description="Mooring line tensions at fairlead",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="TENSION_L06",
                                  description="Mooring line tensions at fairlead",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="TENSION_L09",
                                  description="Mooring line tensions at fairlead",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="TENSION_L10",
                                  description="Mooring line tensions at fairlead",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="TENSION_R01",
                                  description="Mooring line tensions at fairlead",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="X_POS_BL",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Y_POS_BL",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Z_POS_BL",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="X_POS_WL",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Y_POS_WL",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="Z_POS_WL",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ROLL",
                                  description="",
                                  unit="deg",
                                  kind="angle",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="PITCH",
                                  description="",
                                  unit="deg",
                                  kind="angle",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YAW",
                                  description="",
                                  unit="deg",
                                  kind="angle",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XY_POS",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XPOS_MOONP_C",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YPOS_MOONP_C",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_MOONP_C",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XPOS_PDCK_BOW",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YPOS_PDCK_BOW",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_PDCK_BOW",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XPOS_PDCK_STERN",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access) #TODO: Check name

    sensor = client.sensor.create(name="YPOS_PDCK_STERN",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_PDCK_STERN",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XPOS_HELIDECK",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YPOS_HELIDECK",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZPOS_HELIDECK",
                                  description="",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XACC_MOONP_C_CALC",
                                  description="Derived acceleration from motion measurements",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YACC_MOONP_C_CALC",
                                  description="Derived acceleration from motion measurements",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZACC_MOONP_C_CALC",
                                  description="Derived acceleration from motion measurements",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,)

    sensor = client.sensor.create(name="XACC_PDCK_BOW",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YACC_PDCK_BOW",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZACC_PDCK_BOW",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,)

    sensor = client.sensor.create(name="XACC_PDCK_STERN",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YACC_PDCK_STERN",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZACC_PDCK_STERN",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XACC_HELIDECK",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="YACC_HELIDECK",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZACC_HELIDECK",
                                  description="",
                                  unit="m/s^2",
                                  kind="acceleration",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="WAVE_1_CAL",
                                  description="Wave elevation at position 1, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="WAVE_2_CAL",
                                  description="Wave elevation at position 1, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="WAVE_3_CAL",
                                  description="Wave elevation at position 3, zero at SWL - positive upwards",
                                  unit="m",
                                  kind="length",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="XVEL_MOONPOOL",
                                  description="",
                                  unit="m/s",
                                  kind="velocity",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="ZVEL_MOONPOOL",
                                  description="",
                                  unit="m/s",
                                  kind="velocity",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="CURRENT_1",
                                  description="At centre model",
                                  unit="m/s",
                                  kind="velocity",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="CURRENT_2",
                                  description="At centre model",
                                  unit="m/s",
                                  kind="velocity",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="WIND_10",
                                  description="",
                                  unit="m/s",
                                  kind="velocity",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="SLAM_39.5_300",
                                  description="Square slamming panel (2.8*2.8)",
                                  unit="kN",
                                  kind="slamming force",
                                  area = "7.8",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="SLAM_43.5_300",
                                  description="Square slamming panel (2.8*2.8)",
                                  unit="kN",
                                  kind="slamming force",
                                  area = "7.8",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="SLAM_47.5_300",
                                  description="Square slamming panel (2.8*2.8)",
                                  unit="kN",
                                  kind="slamming force",
                                  area = "7.8",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="SLAM_43.5_310",
                                  description="Square slamming panel (2.8*2.8)",
                                  unit="kN",
                                  kind="slamming force",
                                  area = "7.8",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=True,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="FX_WIND/CURR",
                                  description="Wind force tests",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="FY_WIND/CURR",
                                  description="Wind force tests",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="MZ_WIND/CURR",
                                  description="Wind force tests",
                                  unit="kNm",
                                  kind="force", #TODO: Add moment kind
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)

    sensor = client.sensor.create(name="PULLFORCE",
                                  description="Static tests",
                                  unit="kN",
                                  kind="force",
                                  x=position1['x'],
                                  y=position1['y'],
                                  z=None,
                                  is_local=False,
                                  campaign_id=campaign.id,
                                  read_only=restrict_access)





