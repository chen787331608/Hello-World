# -*- coding: utf-8 -*-
# Author: Chen De Long
import scrapy
import json
import requests
import logging


from lagouSpi.items import Website


logger = logging.getLogger("lagou spider")


class Spideri0(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["lagou.com"]
    domain = 'http://www.lagou.com'
    website_possible_httpstatus_list = [403]
    handle_httpstatus_list = [403]

    headers = {
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'www.lagou.com',
                    'Origin': 'http://www.lagou.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Referer': 'http://www.lagou.com',
                    'Proxy-Connection': 'keep-alive',
                    'X-Anit-Forge-Code': '0',
                    'X-Anit-Forge-Token': None
                    }
    cookies_get_url = "https://activity.lagou.com/activityapi/icon/showIcon.json?"
    cookies_str = requests.get(cookies_get_url).cookies['user_trace_token']
    cookies = {
                    'user_trace_token': cookies_str
                    }

    base_url = r'https://www.lagou.com/jobs/positionAjax.json?'
    num = 0
    maxPage = 30
    count = 0
    page = 0

    def start_requests(self):
        while self.num < self.maxPage:
            self.num += 1
            form_data = {'first': 'false', 'pn': str(self.num), 'kd': '数据'}
            print "--------Page %d ------------" % self.num

            yield scrapy.FormRequest(self.base_url,
                                     headers=self.headers,
                                     cookies=self.cookies,
                                     formdata=form_data,
                                     callback=self.parse)

    def parse(self, response):
        if response.body.find('404.png') is not -1:
            req = response.request
            req.meta["change_proxy"] = True
            return req
        else:
            try:
                res_json = json.loads(response.body)['content']['positionResult']
            except:
                print "requestError"
                from scrapy.shell import inspect_response
                inspect_response(response, self)
                return None
            results = res_json['result']
            if self.maxPage == 30:
                self.maxPage = res_json['totalCount']
            items = []
            self.page += 1
            for raw in results:
                self.count = self.count + 1
                item = Website()
                item['company_id'] = raw['companyId']
                item['company_name'] = raw['companyFullName']
                item['create_time'] = raw['createTime']
                item['position_name'] = raw['positionName']
                item['salary'] = raw['salary']
                item['city'] = raw['city']
                item['page'] = self.page
                item['num'] = self.count
                items.append(item)
            file_name = "page%d.json" % self.page
            open(file_name, 'wb').write(str(items))
            return items
