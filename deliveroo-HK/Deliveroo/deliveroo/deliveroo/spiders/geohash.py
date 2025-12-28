import geopy
import mysql.connector
from geopy.geocoders import Nominatim
import geohash2 as geohash
import numpy as np
import deliveroo.df_config as db


def get_bounding_box(city_name):
    """ Get the bounding box of a city using geocoding. """
    geolocator = Nominatim(user_agent="geo_hasher")
    location = geolocator.geocode(city_name, exactly_one=True)
    if location:
        # For simplicity, we're using a rough bounding box around the city center
        # Ideally, you'd get more precise bounding box from a detailed geocoding service or dataset
        return {
            'lat_min': location.latitude - 0.05,
            'lat_max': location.latitude + 0.05,
            'lon_min': location.longitude - 0.05,
            'lon_max': location.longitude + 0.05
        }
    else:
        raise ValueError("City not found")


def generate_geohashes(bbox, precision=11):
    """ Generate all unique geohashes within the bounding box. """
    lat_min, lat_max = bbox['lat_min'], bbox['lat_max']
    lon_min, lon_max = bbox['lon_min'], bbox['lon_max']

    lat_steps = np.linspace(lat_min, lat_max, num=10)  # Adjust number of steps for resolution
    lon_steps = np.linspace(lon_min, lon_max, num=10)  # Adjust number of steps for resolution

    geohashes_set = set()

    for lat in lat_steps:
        for lon in lon_steps:
            hash_value = geohash.encode(lat, lon, precision)
            geohashes_set.add(hash_value)

    return geohashes_set


def main():
    mydb = mysql.connector.connect(
        host=db.host,
        user=db.username,
        password=db.password,
        database=db.database_name
    )

    mycursor = mydb.cursor()
    city_list = ["Hong Kong", "Kowloon", "Sha Tin", "Kowloon City", "Sham Shui Po", "Tin Shui Wai", "Central District",
                 "Tsing Yi Town", "Lam Tin", "San Tung Chung Hang", "Kennedy Town", "Kwai Chung", "Pak Tin Pa",
                 "Cheung Chau", "Choi Hung", "Shek Tong Tsui", "Wang Tau Hom", "Shek Wai Kok", "Tung Tau Tsuen",
                 "Sha Kok Mei", "Sai Wan Ho", "Sai Kung Tuk", "Wan Tau Tong"]
    for c in city_list:
        bbox = get_bounding_box(c)
        geohashes = generate_geohashes(bbox)

        # Print results
        for hash_value in sorted(geohashes):
            print(hash_value)
            item = {}
            item['city'] = c
            item['geo'] = hash_value
            try:
                field_list = []
                value_list = []
                for field in item:
                    field_list.append(str(field))
                    value_list.append(str(item[field]).replace("'", "’"))
                fields = ','.join(field_list)
                values = "','".join(value_list)
                insert_db = f"insert into {db.geohash_data} ( " + fields + " ) values ( '" + values + "' )"
                mycursor.execute(insert_db)
                mydb.commit()
                print(insert_db)
            except Exception as e:
                print(str(e))
        print(f"Total unique geohashes: {len(geohashes)}")


if __name__ == "__main__":
    main()
