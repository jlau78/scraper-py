import logging
from utils.string_utils import string_utils
from utils.handler.handler import handler

su = string_utils()

class ddDtHandler(handler):

    def __init__(self) -> None:
        super().__init__()

    def handle(elements, config):
        """
        Collect multiple key value from the same element type. First value is the 'key', second value is the 'value'.
            eg. <dt>Minimum term</dt> <dt>6 months</dt>

        Args:
            elements (array): List of like elements to process
            config (page_config): page_config config element. eg config['name'] or config['element_name']
        """
        dict = {}
        for element in elements:
            logging.debug('ddDtHandler handle - config:%s, element:%s', config, element)
            keys = []
            alldt = element.find_all('dt', 'feature-list__key')
            for dt in alldt:
                    keys.append(su.clean(dt.text))

            values = []
            alldd = element.find_all('dd', 'feature-list__value')
            for dd in alldd:
                values.append(su.clean(dd.text))

            for i in range(len(keys)):
                logging.debug('create map: index %d -> [%s, %s]', i, keys[i], values[i])
                dict[keys[i]] = values[i]

        logging.info('ddDtHandler result:%s', dict)
        return dict

