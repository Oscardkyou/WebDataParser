from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy.http import HtmlResponse
import random
import time
from fake_useragent import UserAgent
from scrapy.exceptions import NotConfigured
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SeleniumMiddleware:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = uc.Chrome(options=options)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        self.driver.get(request.url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(random.uniform(1, 3))  # Add random delay
        body = self.driver.page_source
        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        self.driver.quit()

class RotateUserAgentAndProxyMiddleware:
    def __init__(self, user_agents, proxies):
        self.user_agents = user_agents
        self.proxies = proxies
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_CHOICES', [])
        proxies = crawler.settings.get('PROXY_POOL', [])
        return cls(user_agents, proxies)

    def process_request(self, request, spider):
        ua = self.ua.random
        request.headers['User-Agent'] = ua
        request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        request.headers['Accept-Language'] = 'en-US,en;q=0.5'
        request.headers['Accept-Encoding'] = 'gzip, deflate, br'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Upgrade-Insecure-Requests'] = '1'
        request.headers['Cache-Control'] = 'max-age=0'
        if self.proxies:
            request.meta['proxy'] = random.choice(self.proxies)

class CustomRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)
        self.max_retry_times = settings.getint('RETRY_TIMES', 10)
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            self.customize_retry(request)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def customize_retry(self, request):
        retry_times = request.meta.get('retry_times', 0)
        if retry_times < self.max_retry_times:
            delay = 2 ** (retry_times + 1) + random.uniform(0, 1)
            time.sleep(delay)
        request.meta['retry_times'] = retry_times + 1
        if 'proxy' in request.meta:
            del request.meta['proxy']

class ScraperMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
