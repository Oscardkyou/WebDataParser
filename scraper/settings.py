BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 1

DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = True

COOKIES_ENABLED = False

TELNETCONSOLE_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
}

SPIDER_MIDDLEWARES = {
   'scraper.middlewares.ScraperMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': None,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': None,
    'rotating_proxies.middlewares.BanDetectionMiddleware': None,
    'scraper.middlewares.SeleniumMiddleware': 800,
    'scraper.middlewares.RotateUserAgentAndProxyMiddleware': 400,
    'scraper.middlewares.CustomRetryMiddleware': 550,
}

ITEM_PIPELINES = {
   'scraper.pipelines.ScraperPipeline': 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODES = [403, 429, 500, 503]

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

# Additional settings to avoid detection
DOWNLOAD_TIMEOUT = 180
REDIRECT_ENABLED = True
AJAXCRAWL_ENABLED = True

# Disable compression to avoid potential issues
COMPRESSION_ENABLED = False

# Use a custom user agent string
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Add delay between batches of requests
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# Limit the depth of crawling
DEPTH_LIMIT = 3

# Enable caching to reduce the number of requests
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # 24 hours

# Respect robots.txt but with a custom policy
ROBOTSTXT_OBEY = True
ROBOTSTXT_USER_AGENT = 'MyBot'

# Proxy settings (you need to add your own proxies)
PROXY_POOL = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080',
]
