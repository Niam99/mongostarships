import json

import pymongo
from pprint import pprint
client = pymongo.MongoClient()
db = client["starwars"]
db.starships.drop()
import requests

db.create_collection("starships")

#function to load the starships from the api into a list fo dictionaries
def loadstarshiplist():
    starshiplist = []
    json_return = requests.get("https://swapi.dev/api/starships/").json()

    for x in json_return["results"]:
        starshiplist.append(x)

    #while loop to go through additional api pages and load the data until there are no more pages
    while json_return["next"] is not None:
        nextpage = json_return["next"]
        json_return = requests.get(nextpage).json()
        for x in json_return["results"]:
            starshiplist.append(x)

    return starshiplist


#this function is used to return the object id of any pilots for each starship
def replacepilots():
    list1 = loadstarshiplist()
    i = 0

    for x in list1:
        stardict = list1[i] #loads each diictionary from the whole list into a dict
        if stardict["pilots"] is not None:
            p = 0
            plist = stardict["pilots"] #creates a list of pilots if it isn't empty
            for x in plist:
                purl = plist[p] #takes the url of the pilot
                json_return = requests.get(purl).json()
                pname = json_return["name"] #determines the pilot name
                objid = db.characters.find_one({"name":pname}, {"_id":1}) #saves the object id of the pilot
                plist[p] = objid #replaces the pilot list item at the current index with the object id
                p += 1
            #saves the pilot list of object ids created by the previous loop in the dict of a starship object
            stardict["pilots"] = plist
        #saves each new dictionary into the position of the old one in the list
        list1[i] = stardict
        i += 1
    return list1

#a function which loops through the new list and saves it to the new starships collection in the database
def load_starship_to_collection():
    mylist = replacepilots()
    for x in mylist:
        db.starships.insert_one(x)


pprint(replacepilots())
load_starship_to_collection()

