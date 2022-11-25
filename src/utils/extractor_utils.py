import logging
import logging.config

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


    def extractElementValue(self, source, element, classname, attribute, text): 
        value = ''
        if text == True:
            if element is None:
                value = source.text
            else:
                value = source.find(element, class_=classname).text
                if value is None:
                    log.warning('element %s has no text value', source)                    
        else:
            if element is None:
                value = source[attribute]
            else:
                elem = source.find(element, class_=classname)
                if elem is not None:
                    value = elem[attribute]
            if value is None:
                log.warning('element %s has no attribute value', source, attribute)                    

        log.debug("Value found for element: %s:%s:%s == %s", element, classname, attribute, value)

        return value

    def verifyValid(self, value):
        print('Verify if value is valid and perform any cleanup')
        return value;
    

    def duplicateCheck(self, key):
        return key;

    
    
