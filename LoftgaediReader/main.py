import csv
import os

STATION_NAME = 0
POLLUTANT_NOTATION = 1
DATE = 3
VALUE = 4
LOCAL_ID = 8
CONCENTRATION = 9


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
    def __init__(self, local_id, name):
        self.local_id = local_id
        self.name = name
        self.pollutants = dict()


file_names = (os.listdir("loftgaedi_data"))

station_dict = dict()

for file_name in file_names:
    with open("loftgaedi_data/" + file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            measurement = Measurement(row[VALUE], row[DATE])
            if row[LOCAL_ID] not in station_dict.keys():
                # Sensor does not exist in dictionary
                sensor = Sensor(row[LOCAL_ID], row[STATION_NAME])
                pollutant = Pollutant(row[POLLUTANT_NOTATION], row[CONCENTRATION])
                pollutant.measurements.append(measurement)
                sensor.pollutants = {row[POLLUTANT_NOTATION]: pollutant}
                station_dict[row[LOCAL_ID]] = sensor
                # station_dict[row[LOCAL_ID]] = {row[POLLUTANT_NOTATION]: [Measurement(row[VALUE],
                                                                                     # row[DATE])]}
            else:
                # Sensor exists
                thing = station_dict[row[LOCAL_ID]].pollutants
                if row[POLLUTANT_NOTATION] not in station_dict[row[LOCAL_ID]].pollutants.keys():
                    # Pollutant does not exist in sensors dictionary
                    pollutant = Pollutant(row[POLLUTANT_NOTATION], row[CONCENTRATION])
                    pollutant.measurements.append(measurement)
                    station_dict[row[LOCAL_ID]].pollutants[row[POLLUTANT_NOTATION]] = pollutant
                    # station_dict[row[LOCAL_ID]][row[POLLUTANT_NOTATION]] = [Measurement(row[VALUE],
                                                                                        # row[DATE])]
                else:
                    # Everything is fine, add measurement
                    station_dict[row[LOCAL_ID]].pollutants[row[POLLUTANT_NOTATION]].measurements.append(measurement)
                    # station_dict[row[LOCAL_ID]][row[POLLUTANT_NOTATION]].append(Measurement(row[VALUE],
                                                                                           # row[DATE],
                                                                                            # row[CONCENTRATION]))

print()
