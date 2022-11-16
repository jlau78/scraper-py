from typing import List
from model.item import item

class listing:

    def __init__(self, id, title, items: List[item]):
        self.id = id
        self.title = title
        self.items = items