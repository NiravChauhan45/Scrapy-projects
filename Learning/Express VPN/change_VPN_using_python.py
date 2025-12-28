from evpn import ExpressVpnApi
import random
import time

with ExpressVpnApi() as api:
    # Todo: Get available locations
    locations = api.locations

    # Filter only USA locations
    usa_locations = [loc for loc in locations if "usa" in loc["name"].lower()]

    if not usa_locations:
        print("No USA locations found!")
    else:
        print("Available USA locations:")
        for loc in usa_locations:
            print(f"- {loc}")

        # Keep switching every 5 seconds
        while True:
            selected_location = random.choice(usa_locations)
            print(f"Connecting to USA location: {selected_location}")
            api.connect(selected_location["id"])  # assuming each location is a dict with an 'id'

            # Stay connected for 5 seconds
            time.sleep(120)
