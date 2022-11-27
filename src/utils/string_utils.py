import logging
import json

class string_utils:

    
    def clean(self, svalue):
        """Clean given string value of \n \r \b " "

        Args:
            svalue (string): String to clean

        Returns:
            _type_: transformed string
        """        

        svalue = str(svalue).replace('\t', '  ')
        svalue = str(svalue).replace('\b', ' ')
        svalue = str(svalue).replace('\r', ' ')
        svalue = str(svalue).replace('\n', '')
        svalue = str(svalue).replace('  ', '')
        # svalue = str(svalue).replace('"', '')
        # svalue = str(svalue).replace('\'', '"')

        # return str(self.encode_ascii(svalue))
        return svalue

    def getJson(self, svalue):
        try:
            jsonstring = json.dumps(svalue)
            print('dump json. result:' + jsonstring)
        except:
            logging.error('Cannot dump json from input:%s', svalue)

    def encode_ascii(self, svalue):
        return str(svalue).encode('ascii', 'ignore')

