# -*- coding: utf-8 -*-
import scrapy
import re


class DmozSpider(scrapy.Spider):
    name = "ces"
    allowed_domains = ["jianshu.com"]
    domain = 'http://jianshu.com'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    }
    base_url = r'http://www.jianshu.com/c/V2CqjW?order_by=added_at&page='
    num = 0

    def start_requests(self):
        while self.num < 4000:
            self.num += 1
            yield scrapy.Request(self.base_url+str(self.num),
                                 headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        li = re.findall(r'<li id.+>[\s\S]+?</li>', response.body)
        for i in li:
            tiAndAu = re.findall(r'>.+</a>', i)
            title = tiAndAu[1][1:-4]
            author = tiAndAu[0][1:-4]
            abstract = re.search(r'<p[\s\S]+?</p>', i).group(0)
            abstract = abstract[27:-9]
#           print 'author:', author, 'title:', title, 'abs:', abstract
            strP = 'author:' + author + '\ntitle:' + title + '\nabs:' + abstract
            open('res.txt', 'a+').write(strP+'\n')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
