# -*- coding: utf-8 -*-
import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for a in response.xpath('//a[text()="(about)"]'):
            yield response.follow(a, self.parse_author)

        # follow pagination links
        for a in response.xpath('//a[text()="Next "]'):
            yield response.follow(a, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'name': extract_with_css('//h3[contains(@class, "author-title")]/text()'),
            'birthdate': extract_with_css('//span[contains(@class, "author-born-date")]/text()'),
            'bio': extract_with_css('//div[contains(@class, "author-description")]/text()'),
        }

