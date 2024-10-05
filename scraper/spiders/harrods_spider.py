import scrapy
from scraper.items import ProductItem
import logging
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class HarrodsSpider(scrapy.Spider):
    name = 'harrods'
    allowed_domains = ['harrods.com']
    start_urls = ['https://www.harrods.com/en-gb/shopping/women', 'https://www.harrods.com/en-gb/shopping/men', 'https://www.harrods.com/en-gb/shopping/kids']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=30,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'li.product-list-item'))
            )

    def parse(self, response):
        products = response.css('li.product-list-item')
        for product in products:
            item = ProductItem()
            item['name'] = product.css('span.product-description::text').get()
            item['brand'] = product.css('span.product-brand::text').get()
            item['price'] = product.css('span.product-price::text').get()
            item['description'] = product.css('span.product-summary::text').get()
            yield item

        next_page = response.css('a.pagination__arrow--next::attr(href)').get()
        if next_page:
            yield SeleniumRequest(
                url=response.urljoin(next_page),
                callback=self.parse,
                wait_time=30,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'li.product-list-item'))
            )
