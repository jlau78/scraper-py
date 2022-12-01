import json
import logging

class page_config:
    """Get config for page elements to extract values from.
        name, container, element_name, class_names, attributes, text
    """

    configs = None

    # def __init__(self) -> None:
    #     pass
      
    def __init__(self, pageconfig_filepath):
        self.configs = self.readPageElements(pageconfig_filepath)

    def readPageElements(self, pageconfig_filepath):
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
        
        # logging.info('readPageElements configdata from:%s, data: %s', pageconfig_filepath, datas)
        return datas

    def allConfigs(self):
        return self.configs

    def value(self, config_key):
        """Get the page_config config value for the given key

        Args:
            config_key (string): key to find config

        Returns:
            _type_: Config value
        """        
        if config_key in self.configs:
            return self.configs[config_key]
        else:
            return None