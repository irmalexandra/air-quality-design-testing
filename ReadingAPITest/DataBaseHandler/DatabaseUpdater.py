import json
import requests
from DataBaseHandler.DatabaseHandler import Database
from Validators.JsonValidator import validateJson

LUFT_DATEN_URL = 'https://data.sensor.community/airrohr/v1/filter/country=IS'
LOFT_GAEDI_LATEST_URL = 'https://api.ust.is/aq/a/getLatest'


def upload_latest_to_db(database):
    loftgaedi_content = json.loads(requests.get("https://api.ust.is/aq/a/getLatest").content)
    for sensor_name in loftgaedi_content.keys():
        if not validateJson(loftgaedi_content[sensor_name]):
            continue
        found_sensor = database.get_one({"local_id": sensor_name})
        parameter_keys = list(loftgaedi_content[sensor_name]["parameters"].keys())
        if found_sensor is None:
            # adding a new sensor to the system
            for key in parameter_keys:
                key_copy = key
                number_of_measurements = len(loftgaedi_content[sensor_name]["parameters"][key_copy].keys()) - 2

                if key.find(".") != -1:
                    key_copy = key.replace(".", ",")
                    loftgaedi_content[sensor_name]["parameters"][key_copy] = \
                        loftgaedi_content[sensor_name]["parameters"][key]
                    del loftgaedi_content[sensor_name]["parameters"][key]

                measurements = dict()
                for measurement_index in range(0, number_of_measurements):
                    # measurement index is loftgaedis "0", "1",...
                    measurement_content = loftgaedi_content[sensor_name]["parameters"][key_copy][
                        str(measurement_index)]
                    measurement_date = measurement_content["endtime"]
                    del measurement_content["endtime"]
                    measurements[measurement_date] = {
                        "value": measurement_content["value"],
                        "verification": measurement_content["verification"]
                    }
                    # fixing the format so the key is the date instead of "0" or "1" etc
                    del loftgaedi_content[sensor_name]["parameters"][key_copy][str(measurement_index)]
                loftgaedi_content[sensor_name]["parameters"][key_copy]["measurements"] = measurements
            database.insert(loftgaedi_content[sensor_name])

        else:
            # if the sensor exists, check for duplicates
            for key in parameter_keys:
                key_copy = key
                number_of_measurements = len(loftgaedi_content[sensor_name]["parameters"][key_copy].keys()) - 2

                if key.find(".") != -1:
                    key_copy = key.replace(".", ",")
                    loftgaedi_content[sensor_name]["parameters"][key_copy] = \
                        loftgaedi_content[sensor_name]["parameters"][key]
                    del loftgaedi_content[sensor_name]["parameters"][key]

                if key_copy in found_sensor["parameters"].keys():
                    found_sensor_measurements = found_sensor["parameters"][key_copy]["measurements"]
                    for measurement_index in range(0, number_of_measurements):
                        # measurement index is loftgaedis "0", "1",...
                        measurement_data = loftgaedi_content[sensor_name]["parameters"][key_copy][str(measurement_index)]
                        if measurement_data["endtime"] not in found_sensor_measurements.keys():
                            # new measurement found
                            found_sensor_measurements[measurement_data["endtime"]] = {
                                "value": measurement_data["value"],
                                "verification": measurement_data["verification"]
                            }
                database.update({"local_id": sensor_name}, {"$set": found_sensor})


my_database = Database("air_quality_data")
upload_latest_to_db(my_database)




















