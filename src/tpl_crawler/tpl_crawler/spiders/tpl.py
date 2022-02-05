import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
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
        branch_table = response.xpath('//*[@id="item-availability"]').get()    #branch_table = branch_table[0]
        #branches = branch_table.xpath('//tbody/tr/td/b/a/text()').getall()
        #print(branch_table)
        branches = re.sub('\s+', ' ', branch_table)
        #print(branches)
        soup = BeautifulSoup(branches, "html.parser")
        branches = soup.select('#item-availability tr td > b > a')
        branch_names = []
        for branch in branches:
            branch_text = branch.get_text().strip()
            if ('Closed' not in branch_text) and ('Toronto Public Library' not in branch_text):
                branch_names.append(branch_text)
        #for branch in branch_table:
        #    print(branch)
        #print(branches)
        page_url = response.url
        return {
            "title": title.strip(),
            "url": page_url,
            "contributors": contributors,
            "branches": branch_names
        }
        #print(title, contributors, branches)