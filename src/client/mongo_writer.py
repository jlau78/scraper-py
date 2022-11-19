import pymongo
import json
import logging

class mongowriter:

    client = pymongo.MongoClient("mongodb://localhost:27017")
    shopDb = client['spareroom']
    collection = shopDb['rooms']

    # def __init__(self):
    #     shopDb = client['spareroom']
    #     colection = shopDb['rooms']


    def addToMongo(self, listings):
        writer = mongowriter()
        # jsondata = json.dumps(listings.toJson(), indent=4)
        # kv = keyvalue_object()
        # jsondata = json.dumps(kv.__dict__ for kv in listings)
        # jsondata = json.dumps(listings, default=obj_dict)
        # for o in listings:
        #     print(o.__class__.__name__)

        print(jsondata)
        writer.write(jsondata)

    def write(self, jsondata):
        logging.info('Data written to mongodb collection:%s', jsondata)
        x = mongowriter.collection.insert_many(jsondata)
        
    def findAll(self):
        rooms = []
        for result in mongowriter.collection.find():
            rooms.append(result)

        return rooms

