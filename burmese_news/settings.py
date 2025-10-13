BOT_NAME = "burmese_news"
SPIDER_MODULES = ["burmese_news.spiders"]
NEWSPIDER_MODULE = "burmese_news.spiders"

ROBOTSTXT_OBEY = True

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