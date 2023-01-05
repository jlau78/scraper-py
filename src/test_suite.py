import logging
import logging.config
from test.test_mongo_call import test_mongo
from client.mongo_spareroom import mongo_spareroom


logging.config.fileConfig('config/log.conf')
log = logging.getLogger('test_suite')

mongo = mongo_spareroom()

# testdata = {"name": "single room wandsworth", "price": "650", "price-unit": "month"}
# mongo.write(testdata)

# rows = mongo.findAll()
# logging.info('Inserted rows: %s', rows)

query = {"itemId": "15598648"}
log.info('find item by itemId: %s', mongo.find(query))


# test_mongo().test_find_one()
test_mongo()

log.info('compleet running tests..******')

