import sys
import logging
import logging.config
from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse, urlencode, parse_qsl, parse_qs

from config.page_config import page_config
from client.mongo_writer import mongowriter
from client.csv_writer import csvwriter
from utils.extractor.html_extractor import soup_extractor
from utils.string_utils import string_utils
from utils.collection_utils import my_dict_wrapper
from service.cache.foreignkey_cache import foreignkey_cache

log = logging.getLogger('Scraper')
su = string_utils()
fkcache = foreignkey_cache()

class scraper:

    def searchByArea(self, area, type, pageconfig_file, max_search_page, search_page_size, container_elem_attr_arr, output_file ):
        """Search rooms by area and type

        Args:
            area (string): Area name
            type (string): type of listing [offered|wanted]
        """        

        try:
            if not area is None or not area == '':
                url = 'https://www.spareroom.co.uk/flatshare/search.pl?nmsq_mode=normal&action=search&max_per_page=&flatshare_type='+type+'&miles_from_max=0&search='+area
                response = requests.get(url)

                # The search request will redirect (302) to the starting search results page. So we get the response's url to scrape the result pages
                responseUrl = response.url #.__getattribute__('search_id')
                logging.info('responseUrl: %s', responseUrl)
                searchIdValue = su.getQSFromUrl(responseUrl, 'search_id')
                baseUrl = "https://www.spareroom.co.uk/flatshare/?&search_id=searchId-value&sort_by=by_day&mode=list&offset=ofset-value" 
                # searchUrl = su.patch_url(baseUrl, search_id=searchIdValue)
                searchUrl = baseUrl.replace('searchId-value', searchIdValue)

                logging.info('Search for area %s => url: %s', area, searchUrl)
                
                self.scrape_listing_pages(area, searchUrl, pageconfig_file, max_search_page, search_page_size, container_elem_attr_arr)
        except:
            logging.error('Failed to get results for the area:%s', area)

 

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

        logging.info('START: Extract elements from:%s, pageconfig:%s', url, pageconfig_filepath)

        listing_dict = {}

        foundElements = self.soup_find(url, container_elem_attr_array)
        logging.info('Found elements:%d for container element:%s', len(foundElements), container_elem_attr_array)

        for elements in foundElements:
            logging.debug('soup_find %s, elements:%s', container_elem_attr_array, elements)

            b = soup_extractor()
            row_dict = {}
            pageconfigs = page_config(pageconfig_filepath)
            headers = []

            for config in pageconfigs.allConfigs():

                c = my_dict_wrapper(config)

                logging.debug('debug: pageconfig %s defined elements to extract values:%s', pageconfig_filepath, c.collection())

                headers.append(c.get('name'))
                value = None

                get_text = c.get('text')
                attributes = c.get('attributes')
                fk = c.get('foreignkey')
                hasMany = c.get('multiple_key_value')
                container = c.get('container')
                name = c.get('name')
                element_name = c.get('element_name')
                class_names = c.get('class_names')

                if not container == None:
                    elements = elements.find(container)
                    log.debug("Nested tag:%s", elements)


                if hasMany is True:
                    elements = self.soup_find(url, [element_name, class_names])
                    extractedString = b.extractMultipleKeyValues( elements, name, element_name)
                    value = extractedString
                    logging.debug('extract hasMany: config:%s, value:%s', c, value)

                elif get_text is True:
                    value = b.extractElementTextValue(name, elements, element_name, class_names)
                    logging.debug('extract text value: config:%s, value:%s', c, value)
                else:
                    value = b.extractElementAttributeValue(name, elements, element_name, class_names, attributes[0])
                    logging.debug('extract attribute value: config:%s, value:%s', c, value)

                if value is None:
                    logging.warn('Fail to extract a value with from the page_config:%s, container element:%s', c, container_elem_attr_array)
                else:
                    logging.debug('extracted value:%s', value)

                row_dict[name] = value

                # TODO: Meke scrape_spareroom_detail_page() call handle generic url, pageconfig_file, and output csv file
                if fk == True:
                    self.handleForeignKeyFound(value)

            if len(row_dict) == 0:
                logging.error('FATAL: Row is empty. Fail to extract any values with the page_config:%s, container element:%s'
                            , c, container_elem_attr_array)
            else:
                listing_dict.update(row_dict)
                # logging.info('listing_dict: %s', listing_dict)

        return listing_dict


    def create_csv_headers(self, headers):
        """Create the headers in the new CSV file"""
        csvwriter().writeHeaderToCsv(output_file, headers)

    def scrape_listing_pages(self, search_identifier, base_url, pageconfig_file, max_num_pages, result_size, container_elem_attr_arr):
        """Iterate through search listing pages and extract articles

        Args:
            search_identifier (string): search identifier for the listing page
            base_url (string): url of the search listing page 
            pageconfig_file (string): page_config config filepath
            max_num_pages (integer): max number of search pages to search
            result_size (integer): number of results per search listing
            container_elem_attr_arr (array): [element, classname] array element of the containing element to find_all on
        """   

        output_file = './data/search-listing-' + search_identifier + '.csv'

        for cur_page in range(1,max_num_pages):
            url = base_url.replace('ofset-value',  str(cur_page * result_size))

            logging.info('scrape_listing_pages for page %s, search url: %s', str(cur_page), url)

            listings = self.extractPageElements(url, pageconfig_file, container_elem_attr_arr)

            if len(listings) > 0:
                logging.debug('Write listings to csv: %s', list(listings.values())) 
                csvwriter().writeToCsv(output_file, listings)

                logging.info('COMPLETE: Extracted elements from given html page:')
                logging.info(url)

                # mongowriter().addToMongo(json.dumps(listings))
            else:
                logging.info('Listing is empty for area: %s', search_identifier)
        
        logging.info('COMPLETED: Extracted all search listings to CSV for %s', search_identifier)

    def scrape_spareroom_detail_page(self, fkid):
        pageconfig_file = 'config/spareroom_room_detail_config.json'
        output_file = './data/sparerooms_room_' + fkid + '.csv'
        url = 'https://www.spareroom.co.uk/flatshare/flatshare_detail.pl?flatshare_id=' + fkid
        room_detail_container_element =  ['div', 'listing listing--property layoutrow']

        logging.info('Get spareroom room detail for flatshareId:%s, output:%s', fkid, output_file)
        self.scrape_item_detail_page(url, pageconfig_file, room_detail_container_element, output_file)


    def scrape_item_detail_page(self, url, pageconfig_file, container_elem_attr_arr, output_file):
        """Scrape item detail page

        Args:
            url (string): url of the item detail
            pageconfig_file (string): page_config config filepath
            container_elem_attr_arr (array): [element, classname] array element of the containing element to find_all on
            output_file (string): CSV file to output extracted data
        """        

        listings = self.extractPageElements(url, pageconfig_file, container_elem_attr_arr)
        logging.debug('Write listings to csv: %s', listings)
        csvwriter().writeToCsv(output_file, listings)

        # mongowriter().addToMongo(json.dumps(listings))

        logging.info('COMPLETED: Extracted item detail page to CSV')
 
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


    def handleForeignKeyFound(self, fkValue):
        """If the foreignkey_cache does not have the given fk, then add the fk to this cache and extract the item details

        Args:
            fkValue (string): foreign key value to handle
        """        
        if fkcache.find(fkValue) is False:
            fkcache.add(fkValue)
            self.scrape_spareroom_detail_page(fkValue) 
        else:
            logging.info('Duplicate found: Item with ForeignKey: %s already extracted', fkValue)
