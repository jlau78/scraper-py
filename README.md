# Study: Python program to scrape sites using the BeautifulSoup library

## Steps

In the terminal 
- mkdir data
- Install dependencies
    pip install beautifulsoup4
    pip install requests
    pip install pymongo
    pip install typing

- Run the scraper: `python3 scrape.py`


scrape.py output sample:

```bash

PS C:\work\code\broex\analysis\scraper-py> python.exe src\scrape.py

2022-11-11 00:24:35,905 - Extractor - INFO - COMPLETE: Extracted elements from given html page:
2022-11-11 00:24:35,905 - Extractor - INFO - https://www.spareroom.co.uk/flatshare/?offset=10&search_id=1177415351&sort_by=by_day&mode=list

```

## Draw.io

Install the Draw.io application to view the ./scraper-overview.drawio diagram.


## Search By Area

The configuration file `config/searchLondonArearList.txt` contains all the areas to search for rooms in London.


## page_config configuration 

The page_config.py processes the configuration file that defines the pgae elements to be extracted.

This page_config contains an array of page elements extraction details. The scraper.extractPageElements() call will traverse the BS4 soup extraction and find each of the page_config elements to process. Below is a sample page_config.element configuration that tells the scraper how to find and extract the element's value.

Example:

```json 

    {
        "name": "feature-list",
        "container": null,
        "multiple_key_value": true,
        "element_name": "dl",
        "class_names": [
            "feature-list"
        ],
        "attributes": null,
        "text": true
    }

```

### Element extraction configuration definitions

- name: "feature-list" > Meta data of the element. Can be used as the header.
- "container": "figure"  > Container element of the element to search for
- 

Either the element's attribute or text value can be extracted.

- text: true > this element text value will be extracted eg. <p>Welcome to my listing</p>
- attributes: "href" > This element's href attribute value is extracted eg <a href='//photo/room/111111/small.jpg>

