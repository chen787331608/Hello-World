# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class Website(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_id = Field()
    company_name = Field()
    create_time = Field()
    position_name = Field()
    salary = Field()
    city = Field()
    page = Field()
    num = Field()
