import pymongo as pymongo

# client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.nujek.mongodb.net/me?retryWrites=true&w=majority")
client = pymongo.MongoClient("mongodb://admin:superSecret@192.168.1.3")
db = client


class Database:
    def __init__(self, name: str):
        self.database = client[name]
        self.collection = self.database["loftgaedi_raw_data"]

    def insert(self, item: dict):
        if self.database:
            self.collection.insert_one(item)

    def insert_many(self, item_list: list):
        if self.database:
            self.collection.insert_many(item_list)

    def remove(self, item_query: dict):
        if self.database:
            self.collection.remove(item_query)

    def update(self, item_query: dict, values: dict):
        if self.database:
            self.collection.update_one(item_query, values)

    def get_many(self, query: dict):
        return_list = []
        for item in self.collection.find_one(query):
            return_list.append(item)
        return return_list

    def get_one(self, query: dict, db_filter=None):
        if filter:
            return self.collection.find_one(query, db_filter)
        return self.collection.find_one(query)
