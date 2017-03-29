#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Chen De Long

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tap.spiders.DmozSpider import DmozSpider

settings = get_project_settings()
process = CrawlerProcess(settings=settings)

process.crawl(DmozSpider)

process.start()
