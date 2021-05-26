import pymongo as pymongo

client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.nujek.mongodb.net/me?retryWrites=true&w=majority")
db = client
print("names")
print(db.list_database_names())
movies_db = client["sample_mflix"]

print(movies_db.name)


print("found thing is ", movies_db["something"].find_one())



def insert_into_something(some_dict: dict):
    return movies_db["something"].insert_one(some_dict)


def find_in_sample_netflix(query: dict):
    return movies_db["movies"].find_one(query)

def find_many_movies(query: dict):
    found_items = []
    for item in movies_db["movies"].find(query, {"title": 1, "_id": 0, "plot": 1}):
        found_items.append(item)
    return found_items


print(find_in_sample_netflix({"year": 1912}), "\n")

for movie in find_many_movies({"year": 1914}):
    print(movie)



