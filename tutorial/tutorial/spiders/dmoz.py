# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.logger.info('Hi, this is an author')

        for quote in response.css('div.quote'):
            item = TutorialItem()
            item['author'] = quote.css('span.text::text').re(r'\“(.*)\”')[0]
            item['text'] = quote.css('small.author::text').extract_first()
            item['link'] = quote.css('span > a::attr(href)').extract_first()
            yield item
