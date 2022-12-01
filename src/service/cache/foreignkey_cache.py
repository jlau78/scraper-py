import logging

class foreignkey_cache:
    """Singleton Cache service to store extracted item keys
    """    

    # Unordered Set (no duplicates) containig item keys
    keys = {''} 

    # def __init__(self) -> None:
    #     pass

    # def __new__(cls: type[Self]) -> Self:
    #     pass
 
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(foreignkey_cache, cls).__new__(cls)
        return cls.instance

    def add(self, key):
        foreignkey_cache.keys.add(key)

    def find(self, key):
        return str(key) in foreignkey_cache.keys
    
