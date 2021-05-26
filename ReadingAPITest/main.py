import requests
import json
import jsonschema
from jsonschema import validate


LUFT_DATEN_URL = 'https://data.sensor.community/airrohr/v1/filter/country=IS'
LOFT_GAEDI_LATEST_URL = 'https://api.ust.is/aq/a/getLatest'


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
        print("is valid ", validateJson(loftgaedi_content[key]))
    return data_base


if __name__ == "__main__":
    load_loftgaedi()
