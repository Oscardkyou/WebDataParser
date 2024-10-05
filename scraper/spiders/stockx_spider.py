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
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="product-tile"]'))
            )

    def parse(self, response):
        products = response.css('div[data-testid="product-tile"]')
        for product in products:
            item = ProductItem()
            item['name'] = product.css('p[data-testid="product-name"]::text').get()
            item['brand'] = product.css('p[data-testid="product-brand"]::text').get()
            item['price'] = product.css('p[data-testid="product-price"]::text').get()
            item['description'] = product.css('p[data-testid="product-description"]::text').get()
            item['sizes'] = product.css('div[data-testid="product-size"] span::text').getall()
            item['color'] = product.css('div[data-testid="product-color"]::text').get()
            item['quantity'] = 'N/A'  # StockX doesn't typically show quantity
            item['details'] = product.css('div[data-testid="product-details"] p::text').getall()
            yield item

        next_page = response.css('a[data-testid="pagination-next-page"]::attr(href)').get()
        if next_page:
            yield SeleniumRequest(
                url=response.urljoin(next_page),
                callback=self.parse,
                wait_time=30,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="product-tile"]'))
            )
