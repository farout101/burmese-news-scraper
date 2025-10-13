BOT_NAME = "burmese_news"
SPIDER_MODULES = ["burmese_news.spiders"]
NEWSPIDER_MODULE = "burmese_news.spiders"

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1.5

# fake user client headers instead of plain http request
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,mm;q=0.8",
}

# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# Set a reasonable download delay to avoid hammering the site
DOWNLOAD_DELAY = 1.0  # seconds between requests

# Configure user-agent to mimic a real browser
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'

# Enable item pipelines (if you plan to store items in a DB or file)
ITEM_PIPELINES = {
    'burmese_news.pipelines.BurmeseNewsPipeline': 300,
}

# Optional: limit concurrent requests
CONCURRENT_REQUESTS = 8

FEED_EXPORT_ENCODING = 'utf-8'

# --------------------------------------------------------------

# Enable Playwright handler
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Optional but helpful:
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000  # 30 seconds
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}