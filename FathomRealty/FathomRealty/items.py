# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy import Field
# from scrapy import Item

class FathomrealtyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()