# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
import os
from datetime import datetime

from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from slugify import slugify


class AmazonItPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for index, image_url in enumerate(item['image_urls']):
            yield Request(image_url, meta={'image_name': f'{item["ASIN"]}_{index+1}.jpg', 'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        # return os.path.join(request.meta['item']['Folder'], request.meta['image_name'])
        return os.path.join(request.meta['image_name'])


class AmazonItPipeline2:
    def process_item(self, item, spider):
        return item
