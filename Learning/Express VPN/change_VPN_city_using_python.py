from evpn import ExpressVpnApi
import random
import time

# ✅ Define the specific target U.S. city servers you want to rotate between
TARGET_CITIES = [
    "new york",
    "new jersey - 1",
    "new jersey - 2",
    "new jersey - 3",
    "chicago",
    "washington",
    "denver"
]

# ✅ How long to stay connected per city (seconds)
CONNECT_DURATION = 60  # e.g., 2 minutes


def main():
    with ExpressVpnApi() as api:
        # Fetch available locations
        locations = api.locations

        # Filter USA locations
        usa_locations = [loc for loc in locations if "usa" in loc["name"].lower()]

        if not usa_locations:
            print("❌ No USA locations found!")
            return

        # Filter only your chosen target city servers
        target_locations = [
            loc for loc in usa_locations
            if any(city in loc["name"].lower() for city in TARGET_CITIES)
        ]

        if not target_locations:
            print("❌ No matching USA city locations found!")
            return

        print("✅ Found target USA city VPN locations:")
        for loc in target_locations:
            print(f"  - {loc['name']} (ID: {loc['id']})")

        # Keep switching between these target cities
        while True:
            selected_location = random.choice(target_locations)
            print(f"\n🔁 Connecting to: {selected_location['name']}")

            try:
                api.connect(selected_location["id"])
                print(f"✅ Connected to {selected_location['name']}")
            except Exception as e:
                print(f"⚠️ Failed to connect to {selected_location['name']}: {e}")
                continue

            # Stay connected for the defined duration
            time.sleep(CONNECT_DURATION)

            # Disconnect before switching to another location
            try:
                api.disconnect()
                print(f"🔌 Disconnected from {selected_location['name']}")
            except Exception as e:
                print(f"⚠️ Disconnect error: {e}")


if __name__ == "__main__":
    main()
