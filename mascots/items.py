# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MascotsItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    images = scrapy.Field()
    image_url = scrapy.Field()
    is_local = scrapy.Field()
    rank = scrapy.Field()
    region = scrapy.Field()
    year = scrapy.Field()