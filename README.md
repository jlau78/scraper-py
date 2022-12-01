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

