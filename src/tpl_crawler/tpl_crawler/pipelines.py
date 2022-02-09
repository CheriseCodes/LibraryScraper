# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TplCrawlerPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None
    def open_spider(self, spider):
        self.conn = sqlite3.connect('tpl_crawler.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Books(book_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,
        contributors TEXT, branches TEXT)''') #TODO: Update branches to JSON

    def close_spider(self, spider):
        self.cursor.execute('''SELECT * FROM Books''')
        print(self.cursor.fetchall())
        self.conn.commit()
        self.conn.close()
    def process_item(self, item, spider):
        print(item['title'])
        self.cursor.execute('''INSERT INTO Books(title, contributors, branches) VALUES (?,?,?)''', (item['title'], item['contributors'], str(item['branches'])))
        return item
