
from abc import ABC, abstractmethod
import pymongo
import json
import logging
from utils.string_utils import string_utils

su = string_utils()
class mongowriter():

    client = pymongo.MongoClient("mongodb://winhost:27017")
    # shopDb = client['spareroom']
    # collection = shopDb['rooms']
    shopDb = None
    collection = None

    def __init__(self, dbname, collection):
        logging.info('Initialise mongowriter, db:%s, collection:%s', dbname, collection)
        self.shopDb = self.client[dbname]
        self.collection = self.shopDb[collection]


    def addToMongo(self, jsondata):
        """Generate JSON from the given CSV data and insert into the Mongodb

        Args:
            datastring (string): CSV data to insert
        """        
        writer = mongowriter()
        self.write(jsondata)

    def write(self, jsondata):
        x = self.collection.insert_one(jsondata)
        logging.info('Write dictionary data to mongodb collection:%s', jsondata['flatshare_id'])

    def update_one(self, query, jsondata):

        self.collection.update_one(query, {'$set': jsondata})

    def upsert(self, query, jsondata):
        """Upsert the record

        Args:
            query (dict): mongo query parameters
            jsondata (dict): data to update 
        """        
        self.collection.update_one(query, {'$set': jsondata}, upsert=True)
        logging.info('upsert doc with id:%s', query)
        
    def findAll(self):
        rooms = []
        for result in self.collection.find():
            rooms.append(result)

        return rooms

    def find(self, query):
        return self.collection.find_one(query)

