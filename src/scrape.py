import sys
import logging
import logging.config
from bs4 import BeautifulSoup
import requests
from config.page_config import page_config
from client.mongo_writer import mongowriter
from client.csv_writer import csvwriter

from utils.extractor_utils import soup_extractor
from model.page_element import page_element
from model.keyvalue_object import keyvalue_object

output_file = "./data/sparerooms.csv"
pageconfig_filepath = 'config/spareroom_search_listing_config.json'

log_config_file = 'config/log.conf'
logging.config.fileConfig(log_config_file)
log = logging.getLogger('Extractor')

def extractPageElements(url):
    """Extract the values from the page elements defined by the page_config"""

    log.info('Extract elements from:%s', url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('li', class_="listing-result")
    # lists = soup.find_all('article', class_="panel-listing-result")
    listings = []

    for list in lists:
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

def create_csv_headers(headers):
    """Create the headers in the new CSV file"""
    csvwriter().writeHeaderToCsv(output_file, headers)

def scrape_listing_pages(base_url, max_num_pages, result_size):
    """Iterate through search listing pages and extract articles"""

    # TODO: temp feature: clean existing before writeToCsv
    csvwriter().temp_remove_existing_csv(output_file)

    for cur_page in range(1,max_num_pages):
        url = base_url + str(cur_page * result_size)
        listings = extractPageElements(url)

        if len(listings) > 0:
            # logging.info('listings: %s', listings)
            csvwriter().writeToCsv(output_file, listings)

            log.info('COMPLETE: Extracted elements from given html page:')
            log.info(url)

            data = page_config.readPageElements(pageconfig_filepath)

            # mongowriter().addToMongo(listings)
    
    log.info('COMPLETED: Extracted all search listings')


url = "https://www.spareroom.co.uk/flatshare/?&search_id=1180008714&sort_by=by_day&mode=list&offset=" 
search_page_size = 10 
max_search_page = 8

scrape_listing_pages(url, max_search_page, search_page_size)
