import logging

class string_utils:

    
    def clean(self, svalue):
        svalue = str(svalue).replace('\t', '  ')
        # str(svalue).replace('\b', ' ')
        # str(svalue).replace('\r', ' ')
        svalue = str(svalue).replace('\n', '')
        svalue = str(svalue).replace('  ', '')
        svalue = str(svalue).replace('"', '')

        return svalue
        # return str(self.encode_ascii(svalue))

    def encode_ascii(self, svalue):
        return str(svalue).encode('ascii', 'ignore')