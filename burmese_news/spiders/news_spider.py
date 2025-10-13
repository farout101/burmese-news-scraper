import scrapy
from burmese_news.items import BurmeseNewsItem

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["myawady.net.mm", "mdn.gov.mm"]

    start_urls = [
        # Education & Technology
        "https://www.myawady.net.mm/education",
        "https://www.myawady.net.mm/tech",
        "https://www.mdn.gov.mm/my/local-education",
        "https://www.mdn.gov.mm/my/international-education",
        # Politics
        "https://www.mdn.gov.mm/my/international-political",
        # Sports
        "https://www.myawady.net.mm/sports",
        "https://www.mdn.gov.mm/my/international-sports",
        # Entertainment
        "https://www.mdn.gov.mm/my/local-entertainment",
        "https://www.mdn.gov.mm/my/international-entertainment",
    ]

    def parse(self, response):
        category = self.detect_category(response.url)
        
        # Extract article links
        links = response.css('a::attr(href)').getall()
        for link in links:
            if any(x in link for x in ['node', 'news', 'article']):
                yield response.follow(link, self.parse_article, meta={'category': category})

    def parse_article(self, response):
        item = BurmeseNewsItem()
        item['text'] = ' '.join(response.css('p::text').getall()).strip()
        item['category'] = response.meta['category']
        item['source'] = response.url.split('/')[2]
        item['url'] = response.url
        yield item

    def detect_category(self, url):
        if 'education' in url or 'tech' in url:
            return "Education & Technology"
        elif 'political' in url:
            return "Politics"
        elif 'sports' in url:
            return "Sports"
        elif 'entertainment' in url:
            return "Entertainment"
        else:
            return "Other"
