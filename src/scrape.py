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
page_num = 1
search_page_size = 10 
baseurl = "https://www.spareroom.co.uk"

# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
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


for i in range(1, 50):
    page_num = i
    url = baseurl + "/flatshare/?offset=" + str(page_num * search_page_size) + "&search_id=1177415351&sort_by=by_day&mode=list";
    listings = extractPageElements(url)

    if len(listings) > 0:
        csvwriter().writeToCsv(output_file, listings)

        log.info('COMPLETE: Extracted elements from given html page:')
        log.info(url)

        data = page_config.readPageElements()
        log.info('readPageElements data: %s', data)

        # mongowriter().addToMongo(listings)

