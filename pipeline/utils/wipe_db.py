import os

os.environ["INQUIRE_MODELTEST_API_USER"] = "ebg"
os.environ["INQUIRE_MODELTEST_API_PASSWORD"] = "pass"
os.environ["INQUIRE_MODELTEST_API_HOST"] = r"http://127.0.0.1:8000"


from modeltestSDK import Client

client = Client()

ans = input(f"You are about to delete all campaigns in DB. URL: {client.config.host}."
            "\nAre you sure you want to wipe db? [Y/N] ")

if ans == "Y":
    key = input("Secret key: ")
    camps = client.campaign.get_all()
    n = len(camps)

    for camp in camps:
        client.campaign.delete(camp.id, parameters={'secret_key':key})

    print(f"Deleted {n} campaigns, DB wiped")
else:
    print("Wipe cancelled")

