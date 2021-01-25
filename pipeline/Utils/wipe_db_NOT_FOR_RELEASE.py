from modeltestSDK import Client

client = Client()

ans = input("You are about to delete all campaigns in DB. \nAre you sure you want to wipe db? [Y/N] ")

if ans == "Y":
    key = input("Secret key: ")
    camps = client.campaign.get_all()
    n = len(camps)

    for camp in camps:
        client.campaign.delete(camp.id, parameters={'secret_key':key})

    print(f"Deleted {n} campaigns, DB wiped")
else:
    print("Wipe cancelled")

