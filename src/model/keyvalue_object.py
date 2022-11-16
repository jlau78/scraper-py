import json

class keyvalue_object:

    def __init__(self):
        pass

    def __init__(self, key, value):
        self.key = key
        self.value = value

    
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)