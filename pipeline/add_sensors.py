from modeltestSDK.resources import Campaign, Sensor
from modeltestSDK.client import SDKclient
from modeltestSDK.utils import TwoWayDict

sensorDict = TwoWayDict()
sensorDict["Wave 1 Moonpool Slot 7 AI0-AI8"] = "wave2"

# Koordinater til sensorene er i enheten meter, og for full skala
# Alle er oppgitt lokalt, dvs. med origo for x- og y i midten av Moonpool, og z ved Base line, altså dypeste punkt på plattformen. (Baseline = vannlinje - draft)
waterline = 0   # [m]
draft_M206 = 29.5   # [m]
draft_M207 = 18     # [m]
deck_height = 47.5  # [m]
VCG_M206 = 14.4     # [m]   I SWACH-specification er denne 17.5
VCG_M207 = 18.2     # [m]   I HE MODU - specification er denne 18.4

def add_sensors(campaign: Campaign, client: SDKclient):

    # M_206_COG sensors. Er usikker på om x og y er null for COG.

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


# M206_acc sensors. Målte verdier fra akselerometer har akselerometeret som origo.

    client.sensor.create(name="M206_acc_pos X",
                         description="Surge position of 6DOF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Y",
                         description="Sway position of 6DOF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Z",
                         description="heave position of 6DOF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Yaw",
                         description="Yaw at position of 6DOF",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Pitch",
                         description="Pitch at position of 6DOF",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_acc_pos Roll",
                         description="Roll at position of 6DOF",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+deck_height+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)


# M206_cof sensors. Vet ikke hvor Centre of Floatation ligger
    client.sensor.create(name="M206_COF X",
                         description="Surge COF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Y",
                         description="Sway COF",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Z",
                         description="Heave COF ",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Yaw",
                         description="COF Yaw ",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Pitch",
                         description="COF Pitch ",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M206_COF Roll",
                         description="COF Roll",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    # Wave sensors

    # Denne skal kanskje være Moonpool istedet for Center. Vent på svar fra Einar
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
                         # 47.5 er høyden til dech på fullskala, i meter
                         is_local=True,  # usikker
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
                         y=(-2750/1000)*75,
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
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 Pitch (Y)',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 Yaw (Z)',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 aks X',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 aks Y',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 aks Z',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 rate X',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 rate Y',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name='MTI 2 rate Z',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=(372.5/1000)*75,
                         z=draft_M206+(60/1000)*75,
                         is_local=True,
                         campaign_id=campaign.id)


# Wagon sensors. Usikker på hva koordinatene skal være
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
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=372.5,
                         z=(47.5 * 1000) / 75 + 60,
                         is_local=True,
                         campaign_id=campaign.id)


# Sensor på fjæren som brukes i pull out test X100. Usikker på hva koordinatene skal være
    client.sensor.create(name='F_pullout Slot 8 AI2 (Single ended)',
                         description='Accelerometer - E',
                         unit='m/s^2',
                         kind='acceleration',
                         x=0,
                         y=372.5,
                         z=(47.5 * 1000) / 75 + 60,
                         is_local=True,
                         campaign_id=campaign.id)



    #M207 sensors

# M207_COG sensors. Usikker på om x- og y skal være 0
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

# M207_acc_pos. Mangler koordinater
    client.sensor.create(name="M207_acc_pos X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Yaw",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Pitch",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_acc_pos Roll",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

# M207_COF. Mangler koordinater
    client.sensor.create(name="M207_COF X",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)
    client.sensor.create(name="M207_COF Y",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Z",
                         description="",
                         unit="mm",
                         kind="length",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Yaw",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Pitch",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)

    client.sensor.create(name="M207_COF Roll",
                         description="",
                         unit="deg",
                         kind="angle",
                         x=0,
                         y=0,
                         z=0,
                         is_local=True,
                         campaign_id=campaign.id)
