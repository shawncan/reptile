# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import TutorialItem


class DemoSpider(CrawlSpider):
    name = "demo"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    rules = (
        Rule(LinkExtractor(allow='/page/\d?/', restrict_css='li.next'), callback='parse_item'),
        Rule(LinkExtractor()),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        for quote in response.css('div.quote'):
            item = TutorialItem()
            item['author'] = quote.css('span.text::text').re(r'\“(.*)\”')[0]
            item['text'] = quote.css('small.author::text').extract_first()
            item['link'] = quote.css('span > a::attr(href)').extract_first()
            yield item
