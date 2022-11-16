import sys
import logging
import logging.config
from bs4 import BeautifulSoup
import requests
import json
from marshmallow import Schema, fields
from csv import writer
from client.mongo_writer import mongowriter

from utils.extractor_utils import soup_extractor
from model.page_element import page_element
from model.keyvalue_object import keyvalue_object

output_file = "./data/sparerooms.csv"
offset = "10"
baseurl = "https://www.spareroom.co.uk"
url = baseurl + "/flatshare/?offset=" + offset + "&search_id=1177415351&sort_by=by_day&mode=list";

# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.config.fileConfig('config/log.conf')
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

        attributes = []
        attributes.append(fillRow('title', title))
        attributes.append(fillRow('shortDesc', shortDesc))
        attributes.append(fillRow('fullDesc', fullDesc))
        attributes.append(fillRow('price', price))
        attributes.append(fillRow('link', link))
        
        # info = [title, price, shortDesc, link]
        listings.append(attributes)

    print(listings)
    return listings

def fillRow(key, value):
    return keyvalue_object(key, value)
        
def readPageElements(url, container_element):
    datas = []
    with open('config/spareroom_search_listing_config.json') as json_file:
        alldata = json.load(json_file)
        for data in alldata:
            # p = page_element
            # p.name = data['name']
            # p.element_name = data['element_name']
            # p.class_names = data['class_names']
            # p.attributes = data['attributes']
            datas.append(data)
    
    return datas


def addToCsv(file, listings):
    with open(file, 'w', encoding='utf8', newline='') as f:
        header = ['Title', 'Price', 'ShortDesc', 'Link']
        thewriter = writer(f)
        thewriter.writerow(header)

        attributes = []
        for info in listings:
            for keyvalue_attr in info:
                attributes.append(keyvalue_attr.value.replace('\n',' '))
            thewriter.writerow(attributes)

def addToMongo(listings):
    writer = mongowriter()
    # jsondata = json.dumps(listings.toJson(), indent=4)
    # kv = keyvalue_object()
    # jsondata = json.dumps(kv.__dict__ for kv in listings)
    # jsondata = json.dumps(listings, default=obj_dict)
    for o in listings:
        print(o.__class__.__name__)


    print(jsondata)
    writer.write(jsondata)

def obj_dict(obj):
    return obj.__dict__

listings = extractPageElements(url)
addToCsv(output_file, listings)
addToMongo(listings)

log.info('COMPLETE: Extracted elements from given html page:')
log.info(url)

data = readPageElements('', '')
log.info(data)
