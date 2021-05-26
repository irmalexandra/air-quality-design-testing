import requests
import json
import jsonschema
from jsonschema import validate
from LoftgaediClasses.Measurement import Measurement
from LoftgaediClasses.Pollutant import Pollutant
from LoftgaediClasses.Sensor import Sensor


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
    returned_data_base = []
    loftgaedi_response = requests.get("https://api.ust.is/aq/a/getLatest")
    loftgaedi_content = json.loads(loftgaedi_response.content)
    for key in loftgaedi_content.keys():
        if(validateJson(loftgaedi_content[key])):
            sensor_dict = loftgaedi_content[key]
            sensor = Sensor(key, sensor_dict["name"], "loftgaedi.is")
            pollutant_dict = dict()
            for pollutant_name in sensor_dict["parameters"].keys():
                pollutant = Pollutant(pollutant_name, sensor_dict["parameters"][pollutant_name]['unit'])
                measurements = []
                for number in range(23):
                    if str(number) in sensor_dict["parameters"][pollutant_name].keys():
                        measurement_dict = sensor_dict["parameters"][pollutant_name][str(number)]
                        measurements.append(Measurement(measurement_dict['value'], measurement_dict['endtime']))

                pollutant.measurements = measurements
                pollutant_dict[pollutant_name] = pollutant

            sensor.pollutants = pollutant_dict
            returned_data_base.append(sensor)

    return returned_data_base


if __name__ == "__main__":
    data_base = load_loftgaedi()
    print(data_base[0].get_dict())
