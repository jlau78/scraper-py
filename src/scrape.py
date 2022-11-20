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

log_config_file = 'config/log.conf'
output_file = "./data/sparerooms.csv"

logging.config.fileConfig(log_config_file)
log = logging.getLogger('Extractor')

def extractPageElements(url):

    log.info('Extract elements from:%s', url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('article', class_="panel-listing-result")
    # print(lists)
    listings = []
    for list in lists:
        b = soup_extractor()

        row = []
        pageconfigs = page_config.readPageElements()
        for c in pageconfigs:
            if c['text'] is True:
                row.append(b.extractElementTextValue(c['name'], list, c['element_name'], c['class_names']))
            else:
                row.append(b.extractElementAttributeValue(c['name'], list, c['element_name'], c['class_names'], c['attributes'][0]))

        listings.append(row)

    return listings

def obj_dict(obj):
    return obj.__dict__

"""Iterate through search listing pages and extract articles"""
def scrape_listing_pages(base_url, max_num_pages, result_size):
    # TODO: temp feature: clean existing before writeToCsv
    csvwriter().temp_remove_existing_csv(output_file)

    for cur_page in range(1,max_num_pages):
        url = base_url + str(cur_page * result_size)
        listings = extractPageElements(url)

        if len(listings) > 0:
            logging.info('listings: %s', listings)
            csvwriter().writeToCsv(output_file, listings)

            log.info('COMPLETE: Extracted elements from given html page:')
            log.info(url)

            data = page_config.readPageElements()

            # mongowriter().addToMongo(listings)
    
    log.info('COMPLETED: Extracted all search listings')


url = "https://www.spareroom.co.uk/flatshare/?&search_id=1177415351&sort_by=by_day&mode=list&offset=" 
search_page_size = 10 
max_search_page = 8

scrape_listing_pages(url, max_search_page, search_page_size)
