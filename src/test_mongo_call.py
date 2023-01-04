import logging
import logging.config

from utils.scraper import scraper
from client.mongo_spareroom import mongo_spareroom

import unittest
# sys.path.insert('..')

class test_mongo(unittest.TestCase):

    logging.config.fileConfig('config/log.conf')
    log = logging.getLogger('test_mongo')

    mongo = mongo_spareroom()

    def test_find_one(self):
        # log.info('find item by itemId: %s', mongo.find(query))
        query = {"itemId": "15598648"}
        row = self.mongo.find(query)

        self.assertIsNotNone(row)

    def test_write_one(self):
        testdata = {"id":"zzz999", "name": "single room wandsworth", "price": "650", "price-unit": "month"}
        # self.mongo.write(testdata)

        query = {"id": "zzz999"}
        doc = self.mongo.find(query)
        self.assertIsNotNone(doc)

    def test_findAll(self):
        rows = self.mongo.findAll()
        # logging.info('Inserted rows: %s', rows)

        self.assertTrue(len(rows) > 1)

