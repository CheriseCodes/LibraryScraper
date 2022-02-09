# LibraryScraper

A web scraper that scrapes public library systems for the given user's holds and checkouts. If needed, a text message can be sent (in plain text or a Google Doc) that informs the user of updates to the status of their library items.

**In progress:**
- [ ] Make features accessible through a Django REST api
- [x] Crawl books from each library system and store the results in a database which can then be accessed through the api (see src/tpl_crawler)

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Usage

An example of how to use this program with the Toronto Public Library System can be found in src/libscrape/tpl-example.py

## Compatible Library Systems

* Pickering Public Library
* Whitby Public Library
* Toronto Public Library 
