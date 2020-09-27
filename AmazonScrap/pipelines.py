# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class AmazonscrapPipeline:
    def process_item(self, item, spider):
        for k, v in item.items():
            if not v:
                item[k]: ''
            elif k == 'Title':
                item[k] = v.strip("\n")
            elif k == 'Description':
                item[k] == v.strip("\n")
                item[k] = re.sub(r'[\\u].{5}', '', v) 
            elif k == 'Price':
                item[k] = re.sub(r'[\\u].{5}', '', v)
        return item
