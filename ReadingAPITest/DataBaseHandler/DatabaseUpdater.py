import json
from datetime import datetime
import requests
import time
from DataBaseHandler.DatabaseHandler import Database
from Validators.JsonValidator import validateJson

LUFT_DATEN_URL = 'https://data.sensor.community/airrohr/v1/filter/country=IS'
LOFT_GAEDI_LATEST_URL = 'https://api.ust.is/aq/a/getLatest'


def upload_latest_to_db(database, content):

    for sensor_name in content.keys():
        if not validateJson(content[sensor_name]):
            with open("log.txt", "a") as log:
                log.write("JsonSchema error on sensor " + sensor_name + " at " + str(datetime.now()) + "\n")
            continue
        found_sensor = database.get_one({"local_id": sensor_name})
        parameter_keys = list(content[sensor_name]["parameters"].keys())
        if found_sensor is None:
            # adding a new sensor to the system
            for key in parameter_keys:
                key_copy = key
                number_of_measurements = len(content[sensor_name]["parameters"][key_copy].keys()) - 2

                if key.find(".") != -1:
                    key_copy = key.replace(".", ",")
                    content[sensor_name]["parameters"][key_copy] = \
                        content[sensor_name]["parameters"][key]
                    del content[sensor_name]["parameters"][key]

                measurements = dict()
                for measurement_index in range(0, number_of_measurements):
                    # measurement index is loftgaedis "0", "1",...
                    measurement_content = content[sensor_name]["parameters"][key_copy][
                        str(measurement_index)]
                    measurement_date = measurement_content["endtime"]
                    del measurement_content["endtime"]
                    measurements[measurement_date] = {
                        "value": measurement_content["value"],
                        "verification": measurement_content["verification"]
                    }
                    # fixing the format so the key is the date instead of "0" or "1" etc
                    del content[sensor_name]["parameters"][key_copy][str(measurement_index)]
                content[sensor_name]["parameters"][key_copy]["measurements"] = measurements
            database.insert(content[sensor_name])

        else:
            # if the sensor exists, check for duplicates
            for key in parameter_keys:
                key_copy = key
                number_of_measurements = len(content[sensor_name]["parameters"][key_copy].keys()) - 2

                if key.find(".") != -1:
                    key_copy = key.replace(".", ",")
                    content[sensor_name]["parameters"][key_copy] = \
                        content[sensor_name]["parameters"][key]
                    del content[sensor_name]["parameters"][key]

                if key_copy in found_sensor["parameters"].keys():
                    found_sensor_measurements = found_sensor["parameters"][key_copy]["measurements"]
                    for measurement_index in range(0, number_of_measurements):
                        # measurement index is loftgaedis "0", "1",...
                        measurement_data = content[sensor_name]["parameters"][key_copy][str(measurement_index)]
                        if measurement_data["endtime"] not in found_sensor_measurements.keys():
                            # new measurement found
                            found_sensor_measurements[measurement_data["endtime"]] = {
                                "value": measurement_data["value"],
                                "verification": measurement_data["verification"]
                            }
                database.update({"local_id": sensor_name}, {"$set": found_sensor})


my_database = Database("air_quality_data")

def get_from_api(api_url):
    content = None
    while content is None:
        try:
            content = json.loads(requests.get(api_url).content)
        except requests.exceptions.Timeout:
            time.sleep(60)
        except requests.exceptions.TooManyRedirects:
            print("Bad URL, exiting.")
            with open("log.txt", "a") as log:
                log.write("Bad url " + api_url + "\n")
            break
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            with open("log.txt", "a") as log:
                log.write("Error" + str(e) + "\n")
            break

    if content is not None:
        with open("log.txt", "a") as log:
            log.write("Accessed " + api_url + " at " + str(datetime.now()) + "\n")
    return content


loftgaedi_content = get_from_api("https://api.ust.is/aq/a/getLatest")
upload_latest_to_db(my_database, loftgaedi_content)




















