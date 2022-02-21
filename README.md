# LibraryScraper

A web scraper that scrapes public library systems for the given user's holds and checkouts. If needed, a text message can be sent (in plain text or a Google Doc) that informs the user of updates to the status of their library items. Now includes a webcrawler that saves the results of a specified TPL query in a database using a custom Django REST API.

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
