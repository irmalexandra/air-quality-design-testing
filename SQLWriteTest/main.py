import os
import requests
import json
import urllib.parse as up
import psycopg2

up.uses_netloc.append("postgres")

man_conn = psycopg2.connect(
    database="pqgxynkd",
    user="pqgxynkd",
    password="ZYwNjR2njVVwzO3xN1qyR6YMhD2e_jPd",
    host="tai.db.elephantsql.com",
    port="5432"
)

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




def display_connection_info():
    cursor = man_conn.cursor()
    print("PostgreSQL server information")
    print(man_conn.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")


def create_tables():
    cursor = man_conn.cursor()
    sensor_table = "sensor"
    gas_table = "gas"
    measurement_table = "measurement"
    drop_table_sensor = "DROP TABLE %s;" % sensor_table;
    drop_table_gas = "DROP TABLE %s;" % gas_table;
    drop_table_measurement = "DROP TABLE %s;" % measurement_table;
    #cursor.execute(drop_table_measurement)
    cursor.execute(drop_table_gas)
    cursor.execute(drop_table_sensor)

    # SQL query to create a new table
    create_sensor_table = '''CREATE TABLE sensor
          (
            ID INT PRIMARY KEY     NOT NULL,
            name           VARCHAR    NOT NULL,
            location         VARCHAR NOT NULL
          ); '''
    # Execute a command: this creates a new table
    cursor.execute(create_sensor_table)

    create_gas_table = '''CREATE TABLE gas 
    (
        ID INT PRIMARY KEY  NOT NULL,
        unit VARCHAR           NOT NULL,
        name VARCHAR           NOT NULL
    ); '''
    cursor.execute(create_gas_table)

    create_measurement_table = '''CREATE TABLE measurement
    (
        ID INT PRIMARY KEY      NOT NULL,
        sensorID INT NOT NULL,
        FOREIGN KEY(sensorID)    NOT NULL,
        REFERENCES sensor(ID),
        gasID INT FOREIGN KEY    NOT NULL,
        date DATE               NOT NULL
    ); '''
    cursor.execute(create_measurement_table)



    man_conn.commit()


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


def insert_loftgaedi(incoming_sensor):
    sensor_name = incoming_sensor.local_id
    location = incoming_sensor.location
    cursor = man_conn.cursor()
    insert_query = """INSERT INTO sensor (ID, name, location) VALUES (1, sensor_name, location) """
    cursor.execute(insert_query)

    man_conn.commit()

def initial_run():
    data_base = load_luft_daten()
    data_base = load_loftgaedi()
    for sensor in data_base:
        insert_loftgaedi(sensor)

if __name__ == '__main__':
    display_connection_info()
    create_tables()
    initial_run()
