import requests
import json
import jsonschema
from jsonschema import validate


LUFT_DATEN_URL = 'https://data.sensor.community/airrohr/v1/filter/country=IS'
LOFT_GAEDI_LATEST_URL = 'https://api.ust.is/aq/a/getLatest'


class Measurement:
    def __init__(self, value, date):
        self.value = value
        self.date = date


class Pollutant:
    def __init__(self, notation, concentration):
        self.notation = notation
        self.concentration = concentration
        self.measurements = []


class Sensor:
    def __init__(self, local_id, name, source):
        self.local_id = local_id
        self.name = name
        self.source = source
        self.pollutants = dict()

def validateJson(jsonData):
    with open("loftgaediSchema.json") as fd:
        loftgaedi_schema = json.load(fd)
    try:
        validate(instance=jsonData, schema=loftgaedi_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


def load_loftgaedi():
    data_base = []
    loftgaedi_response = requests.get("https://api.ust.is/aq/a/getLatest")
    loftgaedi_content = json.loads(loftgaedi_response.content)
    for key in loftgaedi_content.keys():
        if(validateJson(loftgaedi_content[key])):
            sensor_dict = loftgaedi_content[key]
            sensor = Sensor(key, sensor_dict["name"], "loftgaedi.is")
            for pollutant_name in sensor_dict["parameters"].keys():
                pollutant = Pollutant()
            data_base.append(sensor)

    return data_base


if __name__ == "__main__":
    load_loftgaedi()
