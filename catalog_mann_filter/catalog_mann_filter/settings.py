# Scrapy settings for catalog_mann_filter project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "catalog_mann_filter"

SPIDER_MODULES = ["catalog_mann_filter.spiders"]
NEWSPIDER_MODULE = "catalog_mann_filter.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "catalog_mann_filter (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; _fbp=fb.1.1715865419592.468009327; _gcl_au=1.1.213365692.1715865420; OptanonAlertBoxClosed=2024-05-16T13:17:07.235Z; _gid=GA1.2.441703802.1715865427; OptanonConsent=isIABGlobal=false&datestamp=Sat+May+18+2024+19%3A15%3A32+GMT%2B0500+(Pakistan+Standard+Time)&version=6.26.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&geolocation=%3B&AwaitingReconsent=false; _ga=GA1.2.1721240160.1715865420; JSESSIONID=1D935BE448F841BC32822D2682FF97B2; _gat_UA-84202635-11=1; _ga_1WLEWC49T8=GS1.1.1716049445.12.1.1716050306.0.0.0; AWSALBAPP-0=AAAAAAAAAAABA061kEUsB6fk2iX2bNjzJUNlBT6oOR76mm9j85aZtX51JZVAFyrOXs6yrUGYLVbEaSBL+3CAdJFj/GEE+YXH/B1Reik0G4zanO4hO90wijcwSaaZTdG6ylz042VEWTJTKQ==; AWSALBAPP-0=AAAAAAAAAABc6D8wbuvGYEEnbdiXxTSqiVx/MHzJs/F8gm0C9c38IV3sO76m3gMWYLkewiEREWUYD0LeRI5/uFxw6DWHP4AP5EC0UesF1qeVbVaeRO5Df21KbEY4qIu2/NLofSVsJUfNNQ==; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_',
  'priority': 'u=0, i',
  'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "catalog_mann_filter.middlewares.CatalogMannFilterSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "catalog_mann_filter.middlewares.CatalogMannFilterDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "catalog_mann_filter.pipelines.CatalogMannFilterPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# FEED_EXPORT_ENCODING = "iso-8859-9"
FEED_EXPORT_ENCODING = "windows-1254"
# FEED_EXPORT_ENCODING = "UTF-8"
