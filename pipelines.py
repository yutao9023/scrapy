# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem

#处理item中的text
class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    #返回 item或者 DropItem
    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].strip() + '...'
            return item
        else:
            return DropItem('Missing Text')

#将item存到mongodb
class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    #从setttings.py中获取 MONGO_URL和MONGO_DB的值
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    #打开爬虫
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # name = item.__class__.__name__
        self.db['quotes'].insert(dict(item))   #将item插入到数据库中
        return item
    #关闭爬虫
    def close_spider(self, spider):
        self.client.close()

