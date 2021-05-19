from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0.6f5od.mongodb.net/AirQualityTesmailto:contact@Sensor.Communityt?retryWrites=true&w=majority")
db = client.AirQualityTest


def insert_db():
    mycol = db["sensors"]
    my_dict = {"test": "testworked"}
    x = mycol.insert_one(my_dict)
    print(x.inserted_id)
if __name__ == '__main__':
    insert_db()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/