import requests
import json
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0.6f5od.mongodb.net/AirQualityTest?retryWrites=true&w=majority")
db = client.AirQualityTest

LUFT_DATEN_URL = 'https://data.sensor.community/airrohr/v1/filter/country=IS'
LOFT_GAEDI_LATEST_URL = 'https://api.ust.is/aq/a/getLatest'


class Gas:

    def __init__(self, name, info_dict):
        self.name = name


class Coordinates:

    def __init__(self, lat, long, altitude):
        self.lat = lat
        self.long = long
        self.altitude = altitude


class Sensor:

    def __init__(self, info_dict: dict, source=None):
        self.source = source
        self.id = None
        self.location = None
        self.local_id = None

        if source == "loftgaedi":
            self.populate_loftgaedi(info_dict)
        elif source == "luft daten":
            self.populate_luft_daten(info_dict)

    def populate_loftgaedi(self, info_dict):
        self.location = info_dict['name']
        self.local_id = info_dict['local_id']

    def populate_luft_daten(self, info_dict):
        self.id = info_dict['sensor']['id']
        # self.location = Coordinates(info_dict['location']['latitude'], info_dict['location']['longitude'],
        # info_dict['location']['altitude'])

    def to_vars(self):
        return vars(self)


def write_to_db(data):
    sensor_collection = db["sensors"]
    x = sensor_collection.insert_one(vars(data))
    print(x.inserted_id)


def load_loftgaedi():
    data_base = []
    loftgaedi_response = requests.get("https://api.ust.is/aq/a/getLatest")
    loftgaedi_content = json.loads(loftgaedi_response.content)
    for key in loftgaedi_content.keys():
        data_base.append(Sensor(loftgaedi_content[key], "loftgaedi"))
    return data_base


def load_luft_daten():
    data_base = []
    luft_daten = requests.get(LUFT_DATEN_URL).json()
    for daten in luft_daten:
        data_base.append(Sensor(daten, "luft daten"))
    return data_base


def initial_run():
    data_base = load_luft_daten()
    for sensor in data_base:
        write_to_db(sensor)
    print("length is ", len(data_base))
    data_base = load_loftgaedi()
    for sensor in data_base:
        # write_to_db(json.dumps(ModelEncoder().encode(sensor)))
        # write_to_db(json.dumps(sensor, cls=DataEncoder))
        write_to_db(sensor)


initial_run()