# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import requests
from requests.auth import HTTPBasicAuth
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TplCrawlerPipeline:
    def process_item(self, item, spider):
        #print(item['title'])
        api_url = "http://127.0.0.1:8000/books/"
        username = "cherise"
        password = os.environ['TPL_API_PASS']
        # TODO: Save URL in the database
        book = {'title':item['title'], 'contributors':item['contributors'], 'branches':str(item['branches']), 'query':item['query']}
        response = requests.post(api_url,json=book, auth=HTTPBasicAuth(username, password))
        print(response.json())
        #self.cursor.execute('''INSERT INTO Books(title, contributors, branches) VALUES (?,?,?)''', (item['title'], item['contributors'], str(item['branches'])))
        return item
