import sys
import logging
import logging.config
from bs4 import BeautifulSoup
import requests
from csv import writer
from extractor_utils import soup_extractor

output_file = "./data/sparerooms.csv"
offset = "10"
baseurl = "https://www.spareroom.co.uk"
url = baseurl + "/flatshare/?offset=" + offset + "&search_id=1177415351&sort_by=by_day&mode=list";

# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.config.fileConfig('log.conf')
log = logging.getLogger('Extractor')

def extractPageElements(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('article', class_="panel-listing-result")
    # print(lists)
    listings = []
    for list in lists:

        b = soup_extractor()

        title = b.extractElementTextValue('title', list, 'h2', '')
        shortDesc = b.extractElementTextValue('shortDesc', list, 'em', 'shortDescription')
        fullDesc = b.extractElementTextValue('fullDesc', list, 'p', "description").replace('\n', '')
        price = b.extractElementTextValue('price', list, 'strong', "listingPrice")
        link = b.extractElementAttributeValue('link', list, 'a', '', 'href')

        info = [title, price, shortDesc, link]
        listings.append(info)
        # print(info)

    return listings
        

def addToCsv(file, listings):
    with open(file, 'w', encoding='utf8', newline='') as f:
        header = ['Title', 'Price', 'ShortDesc', 'Link']
        thewriter = writer(f)
        thewriter.writerow(header)
        for info in listings:
            thewriter.writerow(info)


listings = extractPageElements(url)
addToCsv(output_file, listings)

log.info('COMPLETE: Extracted elements from given html page:')
log.info(url)
