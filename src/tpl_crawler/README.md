# TPL Crawler

Crawls all results from a search query on torontopubliclibrary.ca and retrieves the title, contributors, and branches each result is available at. Saves the results in a SQLite database by using a custome Django REST API.

## Usage

```bash
cd tpl_crawler/spiders
scrapy runspider tpl.py
```
