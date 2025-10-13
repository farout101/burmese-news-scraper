# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class BurmeseNewsItem(scrapy.Item):
    text = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
