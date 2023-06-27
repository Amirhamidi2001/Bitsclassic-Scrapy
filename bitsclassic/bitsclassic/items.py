# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BitsclassicItem(scrapy.Item):
    title = scrapy.Field()
    # price = scrapy.Field()
    url = scrapy.Field()
    product_exist = scrapy.Field()
    domain = scrapy.Field()
    categories = scrapy.Field()
    currency = scrapy.Field()
