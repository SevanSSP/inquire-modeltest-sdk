"""
A timeseries' data and statistics
"""
from modeltestsdk import Client

with Client() as client:
    campaign = client.campaign.get_by_name("Bream FPSO").scalar()
    test = client.test.get_by_number("3010").filter(campaign_id=campaign.id).scalar()
    ts = test.timeseries()[0]

    window = ts.get_data()                # the default window
    record = ts.get_data(all_data=True)   # the whole record
    stats = ts.get_statistics()           # stored statistics over the default window
    custom = ts.get_statistics(start=2000.0, end=4000.0)  # computed over a custom window, not stored
    print(ts.sensor.name, stats.max, custom.max)
