from .. modeltestSDK import Campaign, SDKclient


data = [
        dict(cname="Electron GmbH2",
             cdescr="Development of floating electrical substation for harsh environment.",
             date=datetime.utcnow(),
             location="Stadt",
             diameter=60,
             scale_factor=1,
             water_density=1025,
             water_depth=900,
             transient=200.),
        dict(cname="Aladdin Oil2",
             cdescr="Development of FPSO for arctic environment.",
             date=datetime.utcnow(),
             location="Sintef",
             diameter=40,
             scale_factor=1,
             water_density=1025,
             water_depth=950,
             transient=200.),
    ]

def main():
    for item in data:
        Campaign.from_dict(item, client)


if __name__ == "__main__":
    client = SDKclient()
    main()
