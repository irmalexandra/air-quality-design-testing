import pymongo as pymongo

CLIENT_URL = "mongodb+srv://user:user@cluster0.nujek.mongodb.net/me?retryWrites=true&w=majority"

client = pymongo.MongoClient(CLIENT_URL)
db = client
print("names")
print(db.list_database_names())
movies_db = client["sample_mflix"]
test_db = client["Airquality_data"]


print(movies_db.name)


print("found thing is ", movies_db["something"].find_one())



def insert_into_something(some_dict: dict):
    return movies_db["something"].insert_one(some_dict)


def find_in_sample_netflix(query: dict):
    return movies_db["movies"].find_one(query)

def find_many_movies(query: dict):
    found_items = []
    for item in movies_db["movies"].find(query, {"title": 1, "_id": 0}).sort("title", -1):
        found_items.append(item)
    return found_items


print(find_in_sample_netflix({"year": 1912}), "\n")

for movie in find_many_movies({"year": 1914}):
    print(movie)

print("------------------------------")

for movie in find_many_movies({"title": {"$regex": "^c|^Amon"}}):
    print(movie)

print("------------------------------")

print(movies_db["something"].delete_one({}).deleted_count, "things deleted")
print(test_db["loftgaedi_raw_data"].find_one({"hello?": "yes"}))
print(test_db["loftgaedi_raw_data"].insert_one({"hello?":"yes"}))
print("------------------------------")

print(movies_db["movies"].find_one({"tomatoes.^*$.meter": 75}))


