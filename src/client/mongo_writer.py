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

    def write(self, jsondata):
        logging.info('Data written to mongodb collection:%s', jsondata)
        x = mongowriter.collection.insert_many(jsondata)
        


    def findAll(self):
        rooms = []
        for result in mongowriter.collection.find():
            rooms.append(result)

        return rooms

