import scrapy
from scrapy.spiders import Spider
import re

query = '?N=37918+4294952073+37844+20206+37751&Ntt=Java+(Computer+program+language)'
class TplSpider(Spider):
    name = 'tpl'
    start_urls = ['https://www.torontopubliclibrary.ca/search.jsp'+ query]
    def parse(self, response):
        book_page_links = response.css('.record-result div.title.align-top > a')
        #print("Book page links:", book_page_links)
        yield from response.follow_all(book_page_links, self.parse_book)
        next_page_link = response.css('.pagination-next > a')
        yield from response.follow_all(next_page_link, self.parse)

    def parse_book(self, response):
        title = response.xpath('//*[@id="bib-detail"]/div[1]/div[2]/div[1]/h1/text()').get()
        contributors = response.xpath('//*[@id="bib-detail"]/div[1]/div[2]/div[3]/a/text()').get()
        branches = response.css('#item-availability tr td > b > a::text').getall()
        branches = ','.join([re.sub('\s+', ' ', branch).strip() for branch in branches if (('Closed' not in branch) and ('Toronto Public Library' not in branch))])
        page_url = response.url
        #print(title)
        yield {
            "title": title.strip(),
            "url": page_url,
            "contributors": contributors,
            "query": query,
            "branches": branches,
        }