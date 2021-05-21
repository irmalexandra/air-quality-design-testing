import os
import psycopg2

man_conn = psycopg2.connect(
    database="pqgxynkd",
    user="pqgxynkd",
    password="ZYwNjR2njVVwzO3xN1qyR6YMhD2e_jPd",
    host="tai.db.elephantsql.com",
    port="5432"
)
local_connection = psycopg2.connect("host=localhost dbname=sensortest user=postgres password=postgres")

def create_tables():
    cursor = local_connection.cursor()

    drop_all_tables = '''DROP TABLE IF EXISTS sensor, pollutant, measurement'''

    cursor.execute(drop_all_tables)

    create_sensor_table = '''CREATE TABLE IF NOT EXISTS sensor
          (
            sensor_id INT              NOT NULL,
            source_name VARCHAR    NOT NULL,
            source_id VARCHAR    NOT NULL,
            latitude FLOAT  NOT NULL,
            longitude FLOAT NOT NULL,
            altitude FLOAT  NOT NULL,
            PRIMARY KEY(sensor_id)
          ); '''
    cursor.execute(create_sensor_table)

    create_pollutant_table = '''CREATE TABLE IF NOT EXISTS pollutant
    (
        pollutant_id INT       NOT NULL,
        unit VARCHAR           NOT NULL,
        pollutant_name VARCHAR           NOT NULL,
        PRIMARY KEY(pollutant_id)
    ); '''
    cursor.execute(create_pollutant_table)

    create_measurement_table = '''CREATE TABLE IF NOT EXISTS measurement
    (
        id INT          NOT NULL,
        sensor_id INT    NOT NULL,
        pollutant_id INT       NOT NULL,
        date DATE       NOT NULL,
        value FLOAT NOT NULL,
        PRIMARY KEY(id),
        FOREIGN KEY(sensor_id) REFERENCES sensor(sensor_id),
        FOREIGN KEY(pollutant_id) REFERENCES pollutant(pollutant_id)
    ); '''
    cursor.execute(create_measurement_table)



    local_connection.commit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_tables()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
