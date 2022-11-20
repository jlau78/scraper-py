import logging
from bs4 import BeautifulSoup

class soup_extractor:
    """BS4 extractor utilities with verification and auditing"""

    # def __init__(self):
    #     pass

    def extractElementTextValue(self, name, source, element, classname): 
        value = self.extractElementValue(source, element, classname, '', True)
        return value

    def extractElementAttributeValue(self, name, source, element, classname, attribute): 
        return self.extractElementValue(source, element, classname, attribute, False)


    def extractElementValue(self, source, element, classname, attribute, text): 
        value = ''
        if text == True:
            value = source.find(element, class_=classname).text
            if value is None:
                logging.warning('element %s has no text value', source)                    
        else:
            elem = source.find(element, class_=classname)
            if elem is not None:
                value = elem[attribute]
            if value is None:
                logging.warning('element %s has no attribute value', source, attribute)                    

        logging.debug("Value found for element: %s:%s:%s == %s", element, classname, attribute, value)

        return value

    def verifyValid(self, value):
        print('Verify if value is valid and perform any cleanup')
        return value;
    

    def duplicateCheck(self, key):
        return key;

    
    
