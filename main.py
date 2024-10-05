import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.stockx_spider import StockXSpider
from scraper.spiders.harrods_spider import HarrodsSpider

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting e-commerce web scraping process")

    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(StockXSpider)
        process.crawl(HarrodsSpider)
        process.start()

        logger.info("E-commerce web scraping process completed")
    except Exception as e:
        logger.error(f"An error occurred during the scraping process: {str(e)}")

if __name__ == "__main__":
    main()
