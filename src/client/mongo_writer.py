import pymongo
import json
import logging
from utils.string_utils import string_utils

su = string_utils()
class mongowriter:

    client = pymongo.MongoClient("mongodb://localhost:27017")
    shopDb = client['spareroom']
    collection = shopDb['rooms']

    # def __init__(self):
    #     shopDb = client['spareroom']
    #     colection = shopDb['rooms']


    def addToMongo(self, datastring):
        """Generate JSON from the given CSV data and insert into the Mongodb

        Args:
            datastring (string): CSV data to insert
        """        
        writer = mongowriter()
        # jsondata = json.dumps(listings.toJson(), indent=4)
        # kv = keyvalue_object()
        # jsondata = json.dumps(kv.__dict__ for kv in listings)
        # jsondata = json.dumps(listings, default=obj_dict)
        # for o in listings:
        #     print(o.__class__.__name__)

                    # row.append(su.getJson(extractedString))
        jsondata = su.getJson(datastring)

        logging.debug('Insert json string into mongodb:%s', jsondata)

        writer.write(jsondata)

    def write(self, jsondata):
        logging.info('Data written to mongodb collection:%s', jsondata)
        x = mongowriter.collection.insert_many(jsondata)
        
    def findAll(self):
        rooms = []
        for result in mongowriter.collection.find():
            rooms.append(result)

        return rooms

