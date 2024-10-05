import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    sizes = scrapy.Field()
    color = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    quantity = scrapy.Field()
