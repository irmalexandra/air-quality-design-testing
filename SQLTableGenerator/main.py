import os
import psycopg2

man_conn = psycopg2.connect(
    database="pqgxynkd",
    user="pqgxynkd",
    password="ZYwNjR2njVVwzO3xN1qyR6YMhD2e_jPd",
    host="tai.db.elephantsql.com",
    port="5432"
)


def create_tables():
    cursor = man_conn.cursor()



    create_location_table = '''CREATE TABLE IF NOT EXISTS location
    (
        locationID INT          NOT NULL,
        latitude FLOAT  NOT NULL,
        longitude FLOAT NOT NULL,
        altitude FLOAT  NOT NULL,
        PRIMARY KEY(locationID)

    );'''
    cursor.execute(create_location_table)

    create_sensor_table = '''CREATE TABLE IF NOT EXISTS sensor
          (
            sensorID INT          NOT NULL,
            locationID INT  NOT NULL,
            name VARCHAR    NOT NULL,
            PRIMARY KEY(sensorID),
            FOREIGN KEY(locationID) REFERENCES location(locationID)
          ); '''
    cursor.execute(create_sensor_table)



    create_gas_table = '''CREATE TABLE IF NOT EXISTS gas 
    (
        gasID INT                 NOT NULL,
        unit VARCHAR           NOT NULL,
        name VARCHAR           NOT NULL,
        PRIMARY KEY(gasID)
    ); '''
    cursor.execute(create_gas_table)

    create_measurement_table = '''CREATE TABLE IF NOT EXISTS measurement
    (
        ID INT          NOT NULL,
        sensorID INT    NOT NULL,
        gasID INT       NOT NULL,
        date DATE       NOT NULL,
        PRIMARY KEY(ID),
        FOREIGN KEY(sensorID) REFERENCES sensor(sensorID),
        FOREIGN KEY(gasID) REFERENCES gas(gasID)
    ); '''
    cursor.execute(create_measurement_table)



    man_conn.commit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_tables()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
