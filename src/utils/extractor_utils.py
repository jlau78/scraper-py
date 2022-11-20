import logging
from bs4 import BeautifulSoup

class soup_extractor:
    """BS4 extractor utilities with verification and auditing"""

    # def __init__(self):
    #     pass

    def extractElementTextValue(self, name, element, obj_, classname): 
        value = self.extractElementValue(element, obj_, classname, '', True)
        return value

    def extractElementAttributeValue(self, name, element, obj_, classname, attribute): 
        return self.extractElementValue(element, obj_, classname, attribute, False)


    def extractElementValue(self, element, object_, classname, attribute, text): 
        value = ''
        if text == True:
            value = element.find(object_, class_=classname).text
            if value is None:
                logging.warning('element %s has no text value', element)                    
        else:
            value = element.find(object_, class_=classname)[attribute]
            if value is None:
                logging.warning('element %s has no attribute value', element, attribute)                    

        logging.debug("Value found for element: %s:%s:%s == %s", object_, classname, attribute, value.replace('\n', ''))

        return value

    def verifyValid(self, value):
        print('Verify if value is valid and perform any cleanup')
        return value;
    

    def duplicateCheck(self, key):
        return key;

    
    
