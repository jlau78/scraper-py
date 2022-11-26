import sys
import logging
import logging.config
from bs4 import BeautifulSoup
import requests
from config.page_config import page_config
from client.mongo_writer import mongowriter
from client.csv_writer import csvwriter
from utils.extractor_utils import soup_extractor
from utils.string_utils import string_utils

log = logging.getLogger('Scraper')
su = string_utils()

class scraper:

    def soup_find(self, url, element_attr):
        """_summary_

        Args:
            url (string): Page url for extraction
            element_attr (array): Array [element, classname] for bs4.find_all to get all elements

        Returns:
            _type_: _description_
        """        

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # lists = soup.find_all('article', class_="panel-listing-result")
        return soup.find_all(element_attr[0], class_= element_attr[1])


    def extractPageElements(self, url, pageconfig_filepath, container_elem_attr_array):
        """
            Extract the values from the page elements defined by the page_config

        Args:
            url (string): Page url for extraction
            pageconfig_filepath (string): page_config config file
            container_elem_attr_arr (array): [element, classname] array element of the containing element to find_all on

        Returns:
            List: List of values extracted from page elements 
        """        

        logging.info('Extract elements from:%s', url)

        listings = []

        for elements in self.soup_find(url, container_elem_attr_array):
            logging.debug('soup_find %s, elements:%s', container_elem_attr_array, elements)
            b = soup_extractor()
            row = []
            pageconfigs = page_config.readPageElements(pageconfig_filepath)
            headers = []
            for c in pageconfigs:
                log.debug('debug: pageconfig defined elements to extract values:%s', c)
                headers.append(c['name'])

                get_text = c['text']

                if not c['container'] == None:
                    elements = elements.find(c['container'])
                    log.debug("Nested tag:%s", elements)

                if c['multiple_key_value'] is True:
                    row.append(self.collectMultipleKeyValueFromSingle(url, elements, c))
                elif get_text is True:
                    logging.debug('extractTextValue: config:%s', c)
                    row.append(b.extractElementTextValue(c['name'], elements, c['element_name'], c['class_names']))
                else:
                    logging.debug('extractAttributeVAlue: config:%s', c)
                    row.append(b.extractElementAttributeValue(c['name'], elements, c['element_name'], c['class_names'], c['attributes'][0]))
            listings.append(row)

        # create_csv_headers(headers)
        return listings

    def collectMultipleKeyValueFromSingle(self, url, elements, config):
        """
        Collect multiple key value from the same element type. First value is the 'key', second value is the 'value'.
            eg. <dt>Minimum term</dt> <dt>6 months</dt>

        Args:
            elements (array): List of like elements to process
            config (page_config): page_config config element. eg config['name'] or config['element_name']
        """
        dict = {}
        features = self.soup_find(url, ['dl', 'feature-list'])
        for element in features:
            logging.debug('collectMultipleKeyValue - config:%s, element:%s', config, element)
            # alldt = element.find_all(config['element_name'], config['class_names'])
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
                dict[keys[i]] = values[i].strip('\n')

        logging.info('collectMultipleKeyValues, map:%s', dict)
        return dict


    def create_csv_headers(self, headers):
        """Create the headers in the new CSV file"""
        csvwriter().writeHeaderToCsv(output_file, headers)

    def scrape_listing_pages(self, base_url, pageconfig_file, max_num_pages, result_size, container_elem_attr_arr, output_file):
        """Iterate through search listing pages and extract articles

        Args:
            base_url (string): url of the search listing page 
            pageconfig_file (string): page_config config filepath
            max_num_pages (integer): max number of search pages to search
            result_size (integer): number of results per search listing
            container_elem_attr_arr (array): [element, classname] array element of the containing element to find_all on
            output_file (string): CSV file to output extracted data
        """   

        for cur_page in range(1,max_num_pages):
            url = base_url + str(cur_page * result_size)

            listings = self.extractPageElements(url, pageconfig_file, container_elem_attr_arr)

            if len(listings) > 0:
                # logging.info('listings: %s', listings)
                csvwriter().writeToCsv(output_file, listings)

                logging.info('COMPLETE: Extracted elements from given html page:')
                logging.info(url)

                # data = page_config.readPageElements(pageconfig_filepath)

                # mongowriter().addToMongo(listings)
        
        logging.info('COMPLETED: Extracted all search listings to CSV')


    def scrape_item_detail_page(self, url, pageconfig_file, container_elem_attr_arr, output_file):
        """Scrape item detail page

        Args:
            url (string): url of the item detail
            pageconfig_file (string): page_config config filepath
            container_elem_attr_arr (array): [element, classname] array element of the containing element to find_all on
            output_file (string): CSV file to output extracted data
        """        

        listings = self.extractPageElements(url, pageconfig_file, container_elem_attr_arr)
        csvwriter().writeToCsv(output_file, listings)

        logging.info('COMPLETED: Extracted page to CSV')


