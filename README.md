# LibraryScraper

## Features
* Automatically retreive your holds and checkouts
* Send a SMS message status updates in plain text or a Google Doc
* Save results of a TPL query in a database for future reference

## Installation

## Option 1: Docker
```bash
docker build --tag libscrape
```

## Option 2: On disk (Unix/Linux)
1. Install [Chrome WebDriver](https://chromedriver.chromium.org/downloads)
2. Install [Python](https://www.python.org/downloads/)
3. [Create a virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
4. Install dependencies from requirements.txt

## Usage
1. Configure an appropriate .env file in src/libscrape
2. Edit src/libscrape/main.py to meet your needs
3. Run one of the following commands:
### Option 1: Docker
```bash
docker run libscrape
```
### Option 2: On Disk (Unix/Linux)
```bash
./send_messages.sh
```
## Sample Code
An example of how to use this program with the Toronto Public Library System can be found in src/libscrape/tpl-example.py

## Compatible Library Systems

* Pickering Public Library
* Whitby Public Library
* Toronto Public Library 
