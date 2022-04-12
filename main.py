import json

import pymongo
from pprint import pprint
client = pymongo.MongoClient()
db = client["starwars"]
db.starships.drop()
import requests

db.create_collection("starships")

#a function which inserts each starship from each page into the starships collection
def loadstarships():
    json_return = requests.get("https://swapi.dev/api/starships/").json()
    for x in json_return["results"]:
        db.starships.insert_one(x)

    json_return = requests.get("https://swapi.dev/api/starships/?page=2").json()
    for x in json_return["results"]:
        db.starships.insert_one(x)

    json_return = requests.get("https://swapi.dev/api/starships/?page=3").json()
    for x in json_return["results"]:
        db.starships.insert_one(x)

    json_return = requests.get("https://swapi.dev/api/starships/?page=4").json()
    for x in json_return["results"]:
        db.starships.insert_one(x)


loadstarships()
pprint(db.starships.find_one({"name":"Jedi Interceptor"},{"_id":0, "name":1, "pilots":1}))
