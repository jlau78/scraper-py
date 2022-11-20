import json
import logging

class page_config:

    json_filepath = 'config/spareroom_search_listing_config.json'
      
    def readPageElements():
        datas = []
        with open(page_config.json_filepath) as json_file:
            alldata = json.load(json_file)
            for data in alldata:
                # p = page_element
                # p.name = data['name']
                # p.element_name = data['element_name']
                # p.class_names = data['class_names']
                # p.attributes = data['attributes']
                datas.append(data)
        
        logging.debug('readPageElements configdata from:%s, data: %s', page_config.json_filepath, data)

        return datas

