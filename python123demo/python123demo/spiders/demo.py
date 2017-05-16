# -*- coding: utf-8 -*-
import scrapy
import re


class DemoSpider(scrapy.Spider):
    name = "demo"
    # allowed_domains = ["python123.io"]
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        List = {}
        stock_list = response.css('.quotebody')
        stock_name = stock_list.css('a[target="_blank"]::text').extract()
        key_list = stock_list.css('a::attr(href)').extract()
        for i in range(len(stock_name)):
            try:
                stock = re.findall(r'[s][hz]\d{6}', key_list[i])[0]
                name = stock_name[i]
                List[name] = stock
                yield List
            except:
                continue

