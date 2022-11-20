from typing import List

from model.attribute import attribute

class item:

    def __init__(self):
        pass

    def item(self, title, shortDesc, fullDesc, price, link, attributes: List[attribute]):
        self.title = title
        self.shortDesc = shortDesc
        self.fullDesc = fullDesc
        self.price = price
        self.link = link
        self.attributes = attributes

