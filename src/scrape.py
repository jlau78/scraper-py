import sys
import logging
import logging.config
from bs4 import BeautifulSoup
import requests
from config.page_config import page_config
from client.mongo_writer import mongowriter
from client.csv_writer import csvwriter

from utils.scraper import scraper
from model.page_element import page_element
from model.keyvalue_object import keyvalue_object


logging.config.fileConfig('config/log.conf')
log = logging.getLogger('Do_Scrape')

scraper = scraper()


# ====================================
# Scrape by Area
# ====================================

output_file = "./data/sparerooms.csv"
pageconfig_file = 'config/spareroom_search_listing_config.json'
url = "https://www.spareroom.co.uk/flatshare/?&search_id=1180008714&sort_by=by_day&mode=list&offset="  # Wandsworth
# url = "https://www.spareroom.co.uk/flatshare/?&search_id=1181896450&sort_by=by_day&mode=list&offset="  # Acton Town
search_page_size = 10 
max_search_page = 8
# TODO: temp feature: clean existing before writeToCsv
csvwriter().temp_remove_existing_csv(output_file)

# scraper.scrape_listing_pages(url, pageconfig_file, max_search_page, search_page_size, ['li', 'listing-result'], output_file)
# scraper.searchByArea('Wandsworth', 'offered', pageconfig_file, max_search_page, search_page_size, ['li', 'listing-result'], output_file)

# ====================================
# Search all London areas and scrape details
# areaListFile='config/searchLondonAreasList.txt'
# ====================================


pageconfig_file = 'config/spareroom_search_listing_config.json'
search_page_size = 10 
max_search_page = 8

areaListFile='config/areaTest.txt'
with open(areaListFile, "r") as areas:
    for line in areas:
        log.info('*********** Scrape item details page for area:%s *****************', line)
        scraper.searchByArea(line, 'offered', pageconfig_file, max_search_page, search_page_size, ['li', 'listing-result'], output_file)

# ====================================
# Test soup_find() 
# ====================================
# log.info('soupfinder: %s', scraper.soup_find(url, ['li',"listing-result"] ))



# ====================================
# Scrape room detail
# ====================================

output_file = "./data/sparerooms_room_16107130.csv"
pageconfig_file = 'config/spareroom_room_detail_config.json'
url = "https://www.spareroom.co.uk/flatshare/flatshare_detail.pl?flatshare_id=16107130" 
# TODO: temp feature: clean existing before writeToCsv
csvwriter().temp_remove_existing_csv(output_file)

# scraper.scrape_item_detail_page(url, pageconfig_file, ['div', 'free_listing'], output_file)


# fn = lambda soup.find_all('li', class_="listing-result")

# Test searchByArea call

