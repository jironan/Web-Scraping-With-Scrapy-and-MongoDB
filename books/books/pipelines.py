# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import hashlib
#itemadapter wraps different data containers to handle them
#in a uniform manner. The package was installed as a dependency of Scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class BooksPipeline:
   #COLLECTION_NAME specifies the name of the MongoDB
   #collection where you want to store the items.
   COLLECTION_NAME = "books"

   def __init__(self, mongo_uri, mongo_db):
       self.mongo_uri = mongo_uri
       self.mongo_db = mongo_db

   @classmethod
   def from_crawler(cls, crawler):
       return cls(
           mongo_uri=crawler.settings.get("MONGODB_URI"),
           mongo_db=crawler.settings.get("MONGODB_DATABASE"),
       )
   
   def open_spider(self, spider):
       self.client = pymongo.MongoClient(self.mongo_uri)
       self.db = self.client[self.mongo_db]

   def close_spider(self, spider):
        self.client.close()

   def process_item(self, item, spider):
        item_id =self.compute_item_id(item)
        item_dict = ItemAdapter(item).asdict()

        self.db[self.COLLECTION_NAME].update_one(
           filter= {"id": item_id}, 
           update={"$set": item_dict}, 
           upsert=True
        )
        return item
        
   def compute_item_id(self, item):
       url = item["url"]
       return hashlib.sha256(url.encode("utf-8")).hexdigest()