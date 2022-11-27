import json
import logging

class page_config:
    """Get config for page elements to extract values from.
        name, container, element_name, class_names, attributes, text
    """
      
    def readPageElements(pageconfig_filepath):
        """
        Read the page_config file and get all the page_config attributes

        Returns:
            Array: Array of page_config attributes

        Args:
            pageconfig_filepath (String): page_config filepath

        """

        datas = []
        with open(pageconfig_filepath) as json_file:
            alldata = json.load(json_file)
            for data in alldata:
                datas.append(data)
        
        logging.debug('readPageElements configdata from:%s, data: %s', pageconfig_filepath, data)

        return datas

