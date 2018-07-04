# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = [
            'http://quotes.toscrape.com/',
        ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split('/')[-2]
    #     filename = f'quotes-{page}.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log(f'saved file {filename}')

    def parse(self, response):
        for quote in response.xpath('//div[contains(@class, "quote")]'):
            yield {
                'text': quote.xpath('span[contains(@class, "text")]/text()').extract_first(),
                'author': quote.xpath('span/small[contains(@class, "author")]/text()').extract_first(),
                'tags': quote.xpath('div[contains(@class, "tags")]/a[contains(@class, "tag")]/text()').extract(),
            }
        # next_page = response.xpath('//a[text()="Next "]/@href').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
        # for href in response.xpath('//a[text()="Next "]/@href'):
        #     yield response.follow(href, callback=self.parse)
        # response.follow auto picks up href attribute if <a> tag is provided
        for a in response.xpath('//a[text()="Next "]'):
            yield response.follow(a, callback=self.parse)

