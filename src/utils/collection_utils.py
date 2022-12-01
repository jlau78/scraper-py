
class my_dict_wrapper:

    dict = None

    def __init__(self, dict) -> None:
        self.dict = dict
    
    def get(self, key):
        """If the given key exists in the dictionary return its value else return None

        Args:
            key (key): key to get value

        Returns:
            string: value of the key
        """        
        if key in self.dict:
            return self.dict[key]
    
    def collection(self):
        return self.dict