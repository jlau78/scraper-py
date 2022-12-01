import logging
import json
from urllib.parse import urlparse, urlencode, parse_qsl, parse_qs

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

    def getQSFromUrl(self, url, query_string):
        """Get the query string value from the given url

        Args:
            url (string): url to search query string
            query_string (string): query_string to read

        Returns:
            _type_: _description_
        """        

        parse_result = urlparse(url)
        dict_result = parse_qs(parse_result.query)
        return dict_result[query_string][0]


    def patch_url(self, url, **kwargs):
        """Replace the query string value for the given url

        Args:
            url (string): url containing the query string to update
            kwargs (string): key value argument to replace eg. search_id = '1234566'

        Returns:
            string: given url with the query string replaced
        """        

        # TODO: Bug urlencode appears to cause problems as encountered in the spareroom url querystring &offset=

        return urlparse(url)._replace(query=urlencode(
            dict(parse_qs(urlparse(url).query), **kwargs))).geturl()
    
