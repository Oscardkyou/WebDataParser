import scrapy
from scraper.items import ProductItem
import logging
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class StockXSpider(scrapy.Spider):
    name = 'stockx'
    allowed_domains = ['stockx.com']
    start_urls = ['https://stockx.com/sneakers', 'https://stockx.com/streetwear', 'https://stockx.com/collectibles']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=30,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-111hzm2'))
            )

    def parse(self, response):
        products = response.css('div.css-111hzm2')
        for product in products:
            item = ProductItem()
            item['name'] = product.css('p.chakra-text.css-3lpefb::text').get()
            item['brand'] = product.css('p.chakra-text.css-1juslt3::text').get()
            item['price'] = product.css('p.chakra-text.css-nzy192::text').get()
            item['description'] = product.css('p.chakra-text.css-1l3zk6f::text').get()
            yield item

        next_page = response.css('a[data-testid="pagination-next-page"]::attr(href)').get()
        if next_page:
            yield SeleniumRequest(
                url=response.urljoin(next_page),
                callback=self.parse,
                wait_time=30,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-111hzm2'))
            )
