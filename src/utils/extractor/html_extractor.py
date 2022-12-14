import logging
import logging.config

from utils.handler.dlHandler import dlHandler
from utils.handler.ulHandler import ulHandler

log = logging.getLogger('Extractor')

class soup_extractor:
    """BS4 extractor utilities with verification and auditing"""

    # def __init__(self):
    #     pass

    def extractElementTextValue(self, name, source, element, classname): 
        value = self.extractElementValue(source, element, classname, '', True)
        return value

    def extractElementAttributeValue(self, name, source, element, classname, attribute): 
        return self.extractElementValue(source, element, classname, attribute, False)

    def extractMultipleKeyValues(self, elements, name, element_name):
        """Extract the values from multiple child elements. 

        Args:
            elements (array): List of page elements to process
            name (string): Name of this extract used as the key/header value
            element_name (string): Parent element whose child elements' values will be extracted

        Returns:
            _type_: Dict of multiple KV pairs eg attributes for a <dl> child elements
        """        
        if element_name == 'dl':
            extractedString = dlHandler.handle(elements, element_name)
        elif element_name == 'ul':
            # TODO: Move to own method and handle element_name and class
            extractedString = ulHandler.handle(elements, element_name)
        
        return extractedString


    def extractElementValue(self, source, element, classname, attribute, text): 
        value = ''
        if text == True:
            if element is None:
                value = source.text
            else:
                logging.debug('extract text from element:%s, class:%s, source:', element, classname)
                value = None
                elem = source.find(element, class_=classname)
                if not elem is None:
                    value = elem.text
                    
                if value is None:
                    log.warning('element %s has no text value', source)                    
        else:
            if element is None:
                value = source[attribute]
            else:
                elem = source.find(element, class_=classname)
                if elem is not None:
                    # logging.debug('extract attr %s from element:%s', attribute, elem)
                    value = elem[attribute]
            if value is None:
                log.warning('element %s has no attribute value', source, attribute)                    

        log.debug("Value found for element: %s:%s:%s == %s", element, classname, attribute, value)

        return value

    def verifyValid(self, value):
        print('Verify if value is valid and perform any cleanup')
        return value;
    
    # Cache of extracted items' keys used for duplicate checks
    extractedKeys = []

    def duplicateCheck(self, key):
        alreadyExist = false
        

        return key;

    
