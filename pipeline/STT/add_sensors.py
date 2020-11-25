from modeltestSDK.resources import Campaign, Sensor
from modeltestSDK.client import SDKclient
from modeltestSDK.utils import TwoWayDict

sensorDict = TwoWayDict()
sensorDict["Wave 1 Moonpool Slot 7 AI0-AI8"] = "wave2"

# Coordinates for the sensors are give for full scale in meters
# All coordinates are given with origo for x- and y in the center of the moonpool, and z at Base line (deepest point on platform)
draft_M206 = 29.5   # [m]
draft_M207 = 18     # [m]
deck_height = 47.5  # [m]
VCG_M206 = 14.4     # [m]   # This is 17.5 meters in SWACH-specification report
VCG_M207 = 18.2     # [m]   # This is 18.4 meters in HE MODU specification report

# TODO: Verify all coordinates
def add_sensors(campaign: Campaign, client: SDKclient):

    # M206 sensors
    # M_206_COG sensors

    client.sensor.create(name="M206_COG X",
                         description="Surge COG",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=VCG_M206,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M206_COG Y",
                         description="Sway COG",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=VCG_M206,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M206_COG Z",
                         description="Heave COG",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=VCG_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COG Yaw",
                         description="COG Yaw",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=VCG_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COG Pitch",
                         description="COG Pitch",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=VCG_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COG Roll",
                         description="COG Roll",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=VCG_M206,
                         is_local=True,
                         campaign_id=campaign.id)

# M206_acc sensors. Accelerometer is origo for these sensors.
    client.sensor.create(name="M206_acc_pos X",
                         description="Surge position of 6DOF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Y",
                         description="Sway position of 6DOF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Z",
                         description="heave position of 6DOF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Yaw",
                         description="Yaw at position of 6DOF",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Pitch",
                         description="Pitch at position of 6DOF",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Roll",
                         description="Roll at position of 6DOF",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

# M206_cof sensors. Not sure what coordinates are for centre of floatation

    client.sensor.create(name="M206_COF X",
                         description="Surge COF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Y",
                         description="Sway COF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Z",
                         description="Heave COF ",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Yaw",
                         description="COF Yaw ",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Pitch",
                         description="COF Pitch ",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Roll",
                         description="COF Roll",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    # Wave sensors
    # TODO: cant find this sensor
    client.sensor.create(name="Wave 1 Center Slot 7 AI0-AI8",
                         description="Relative wave probe for moonpool",
                         unit="mm",
                         kind="length",
                         x=(-117/1000)*75,
                         y=0,
                         z=None,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave 1 Moonpool Slot 7 AI0-AI8',
                         description='Wave model moonpool - A',
                         unit='mm',
                         kind='length',
                         x=(-117/1000)*75,
                         y=0,
                         z=None,
                         is_local=True,     # Not sure if these are local or global
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave 2 Front Model Slot 7 AI1-AI9',
                         description='Wave model front - B',
                         unit='mm',
                         kind='length',
                         x=(755/1000)*75,
                         y=0,
                         z=None,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave 3 Front Slot 7 AI2-AI10',
                         description='Wave front - C',
                         unit='mm',
                         kind='length',
                         x=(1925/1000)*75,
                         y=(370/1000)*75,
                         z=None,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave 4 Side Slot 7 AI4-AI12',
                         description='Wave side - D',
                         unit='mm',
                         kind='length',
                         x=(1095/1000)*75,
                         y=-(2750/1000)*75,
                         z=None,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wave US Front Slot 7 AI3-AI11',
                         description='Wave side US - F',
                         unit='mm',
                         kind='length',
                         x=(1925/1000)*75,
                         y=(610/1000)*75,
                         z=None,
                         is_local=True,
                         campaign_id=campaign.id)

# Force sensors (in moorings placed on waterline)

    client.sensor.create(name='F_BB_Front_Slot 8 AI5',
                         description='Force BB Front',
                         unit='N',
                         kind='force',
                         x=(4000/1000)*75,
                         y=(-4000/1000)*75,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='F_SB_Front_Slot 8 AI6',
                         description='Force SB Front',
                         unit='N',
                         kind='force',
                         x=(4000/1000)*75,
                         y=(3800/1000)*75,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='F_BB_Aft_ Slot 8 AI4',
                         description='Force BB Aft',
                         unit='N',
                         kind='force',
                         x=(-4600/1000)*75,
                         y=(-4000/1000)*75,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='F_SB_Aft_Slot 8 AI3',
                         description='Force SB Aft',
                         unit='N',
                         kind='force',
                         x=(-4600/1000)*75,
                         y=(3800/1000)*75,
                         z=draft_M206,
                         is_local=True,
                         campaign_id=campaign.id)

    #MTI 2 sensors (accelerometer)

    client.sensor.create(name='MIT 2 Roll (X)',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 Pitch (Y)',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 Yaw (Z)',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 aks X',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 aks Y',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 aks Z',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 rate X',
                         description='Accelerometer - E',
                         unit='deg/s',
                         kind='angular velocity',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 rate Y',
                         description='Accelerometer - E',
                         unit='deg/s',
                         kind='angular velocity',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 rate Z',
                         description='Accelerometer - E',
                         unit='deg/s',
                         kind='angular velocity',
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

# Wagon sensors. Not sure what the coordinates should be for these

    client.sensor.create(name='Wagon Master Position',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=372.5,
                         z=(47.5 * 1000) / 75 + 60,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='Wagon Master Speed',
                         description='Accelerometer - E',
                         unit='m/s',
                         kind='velocity',
                         x=0,
                         y=372.5,
                         z=(47.5 * 1000) / 75 + 60,
                         is_local=True,
                         campaign_id=campaign.id)

    # Sensor on the spring that is used for pull out test X100. Not sure what coordinates should be

    client.sensor.create(name='F_pullout Slot 8 AI2 (Single ended)',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=372.5,
                         z=(47.5 * 1000) / 75 + 60,
                         is_local=True,
                         campaign_id=campaign.id)



    # M207 sensors
    # M207_COG sensors. Not sure if x and y should be zero

    client.sensor.create(name="M207_COG X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=VCG_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COG Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=VCG_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COG Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=VCG_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COG Yaw",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=VCG_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COG Pitch",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=VCG_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COG Roll",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=VCG_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    # M207_acc_pos. Need coordinates
    # TODO: check whether STT has accounted for deck height of 39.5 or not (49.5) in their output
    client.sensor.create(name="M207_acc_pos X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Yaw",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Pitch",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Roll",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    # M207_COF. Needs coordinates
    client.sensor.create(name="M207_COF X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=draft_M207,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M207_COF Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=draft_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=draft_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Yaw",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=draft_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Pitch",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=draft_M207,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Roll",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=draft_M207,
                         is_local=True,
                         campaign_id=campaign.id)
