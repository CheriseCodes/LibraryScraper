import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class TplSpider(CrawlSpider):
    # TODO: Copy this pagination pattern: https://docs.scrapy.org/en/latest/intro/tutorial.html?highlight=pagination#more-examples-and-patterns
    name = 'tpl'
    allowed_domains = ['torontopubliclibrary.ca']
    start_urls = ['https://www.torontopubliclibrary.ca/search.jsp?N=37918+4294952073+37844+20206+37751&Ntt=Python+(Computer+program+language)']
    custom_settings = {
        'DEPTH_LIMIT': '1',
    }
    rules = [Rule(LinkExtractor(allow=r'https:\/\/www\.torontopubliclibrary\.ca\/detail\.jsp\?Entt='), callback='parse_info', follow=True)]
    def parse_info(self, response):
        #print(response.text)
        title = response.xpath('//*[@id="bib-detail"]/div[1]/div[2]/div[1]/h1/text()').get()
        contributors = response.xpath('//*[@id="bib-detail"]/div[1]/div[2]/div[3]/a/text()').get()
        branches = response.css('#item-availability tr td > b > a::text').getall()
        branches = [re.sub('\s+', ' ', branch).strip() for branch in branches if (('Closed' not in branch) and ('Toronto Public Library' not in branch))]
        page_url = response.url
        yield {
            "title": title.strip(),
            "url": page_url,
            "contributors": contributors,
            "branches": branches
        }