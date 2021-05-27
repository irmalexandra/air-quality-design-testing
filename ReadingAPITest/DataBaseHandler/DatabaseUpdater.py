import json
import requests
from DataBaseHandler.DatabaseHandler import Database

LUFT_DATEN_URL = 'https://data.sensor.community/airrohr/v1/filter/country=IS'
LOFT_GAEDI_LATEST_URL = 'https://api.ust.is/aq/a/getLatest'


my_database = Database("Loftgaedi_raw_data")


def upload_latest_to_db(database):
    loftgaedi_response = requests.get("https://api.ust.is/aq/a/getLatest")
    loftgaedi_content = json.loads(loftgaedi_response.content)
    for sensor_name in loftgaedi_content.keys():
        the_keys = list(loftgaedi_content[sensor_name]["parameters"].keys())
        for key in the_keys:
            dot_index = key.find(".")
            if dot_index != -1:
                new_key = key.replace(".", ",")
                loftgaedi_content[sensor_name]["parameters"][new_key] = loftgaedi_content[sensor_name]["parameters"][key]
                del loftgaedi_content[sensor_name]["parameters"][key]

    database.insert(loftgaedi_content)


upload_latest_to_db(my_database)



















