import sys
import logging
import logging.config
from bs4 import BeautifulSoup
import requests
from config.page_config import page_config
from client.mongo_writer import mongowriter
from client.csv_writer import csvwriter
from utils.extractor_utils import soup_extractor

log = logging.getLogger('Scraper')

class scraper:

    def soup_find(self, url, element_attr):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # lists = soup.find_all('article', class_="panel-listing-result")
        return soup.find_all(element_attr[0], class_= element_attr[1])


    def extractPageElements(self, url, pageconfig_filepath, container_elem_attr_array):
        """Extract the values from the page elements defined by the page_config"""

        log.info('Extract elements from:%s', url)

        listings = []

        for list in self.soup_find(url, container_elem_attr_array):
            b = soup_extractor()
            row = []
            pageconfigs = page_config.readPageElements(pageconfig_filepath)
            headers = []
            for c in pageconfigs:
                log.debug('debug: pageconfig defined elements to extract values:%s', c)
                headers.append(c['name'])

                get_text = c['text']

                if not c['container'] == None:
                    list = list.find(c['container'])
                    log.debug("Nested tag:%s", list)

                if get_text is True:
                    row.append(b.extractElementTextValue(c['name'], list, c['element_name'], c['class_names']))
                else:
                    row.append(b.extractElementAttributeValue(c['name'], list, c['element_name'], c['class_names'], c['attributes'][0]))
            listings.append(row)

        # create_csv_headers(headers)
        return listings

    def create_csv_headers(self, headers):
        """Create the headers in the new CSV file"""
        csvwriter().writeHeaderToCsv(output_file, headers)

    def scrape_listing_pages(self, base_url, pageconfig_file, max_num_pages, result_size, container_elem_attr_arr, output_file):
        """Iterate through search listing pages and extract articles"""

        # TODO: temp feature: clean existing before writeToCsv
        csvwriter().temp_remove_existing_csv(output_file)

        for cur_page in range(1,max_num_pages):
            url = base_url + str(cur_page * result_size)

            listings = self.extractPageElements(url, pageconfig_file, container_elem_attr_arr)

            if len(listings) > 0:
                # log.info('listings: %s', listings)
                csvwriter().writeToCsv(output_file, listings)

                log.info('COMPLETE: Extracted elements from given html page:')
                log.info(url)

                # data = page_config.readPageElements(pageconfig_filepath)

                # mongowriter().addToMongo(listings)
        
        log.info('COMPLETED: Extracted all search listings to CSV')


    def scrape_single_page(self, url, pageconfig_file, container_elem_attr_arr, output_file):
        # TODO: temp feature: clean existing before writeToCsv
        csvwriter().temp_remove_existing_csv(output_file)

        listings = self.extractPageElements(url, pageconfig_file, container_elem_attr_arr)
        csvwriter().writeToCsv(output_file, listings)

        log.info('COMPLETED: Extracted page to CSV')


