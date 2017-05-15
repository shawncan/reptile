# -*- coding: utf-8 -*-
import scrapy
import re


class DemoSpider(scrapy.Spider):
    name = "demo"
    # allowed_domains = ["python123.io"]
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        List = {}
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r'[s][hz]\d{6}', href)[0]
                yield stock
            except:
                continue
