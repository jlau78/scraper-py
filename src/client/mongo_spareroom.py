
from client.mongo_writer import mongowriter 

class mongo_spareroom(mongowriter):

    dbname = 'spareroom'
    collection = 'rooms'

    def __init__(self, dbname, collection):
        super().__init__(dbname, collection)

    def __init__(self):
        super().__init__(self.dbname, self.collection)


