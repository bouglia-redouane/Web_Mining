# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PostItem(scrapy.Item):
    job_title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    job_url = scrapy.Field()
    company_url = scrapy.Field()
    date = scrapy.Field()
    job_description = scrapy.Field()
