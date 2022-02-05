import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


class TplSpider(CrawlSpider):
    name = 'tpl'
    allowed_domains = ['torontopubliclibrary.ca']
    start_urls = ['https://www.torontopubliclibrary.ca/search.jsp?N=37918+4294952073+37844+20206+37751&Ntt=Python+(Computer+program+language)']
    custom_settings = {
        'DEPTH_LIMIT': '1',
    }
    rules = [Rule(LinkExtractor(allow=r'https:\/\/www\.torontopubliclibrary\.ca\/detail\.jsp\?Entt='), callback='parse_info', follow=True)]
    def parse_info(self, response):
        title = response.xpath('//*[@id="bib-detail"]/div[1]/div[2]/div[1]/h1/text()').get()
        contributors = response.xpath('//*[@id="bib-detail"]/div[1]/div[2]/div[3]/a/text()').get()
        #branch_table = response.xpath('//*[@id="item-availability"]').get()     #branch_table = branch_table[0]
        #print(branch_table)
        page_url = response.url
        return {
            "title": title.strip(),
            "url": page_url,
            "contributors": contributors,
            #"branches": branches
        }
        #print(title, contributors, branches)