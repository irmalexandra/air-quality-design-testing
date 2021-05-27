import pymongo as pymongo

client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.nujek.mongodb.net/me?retryWrites=true&w=majority")
db = client


class Database:
    def __init__(self, name: str):
        self.database = client[name]
        self.collection = self.database["yes"]

    def insert(self, item: dict):
        if self.database:
            self.collection.insert_one(item)

    def insert_many(self, item_list: list):
        if self.database:
            self.collection.insert_many(item_list)

    def remove(self, item_query: dict):
        if self.database:
            self.collection.remove(item_query)

    def get_many(self, query: dict):
        return_list = []
        for item in self.collection.find(query):
            return_list.append(item)
        return return_list

    def get_one(self, query: dict):
        return self.collection.find(query)
