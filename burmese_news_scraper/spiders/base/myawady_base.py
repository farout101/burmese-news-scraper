import scrapy
import re
from burmese_news_scraper.items import BurmeseNewsItem

class MyawadyBaseSpider(scrapy.Spider):
    allowed_domains = ["myawady.net.mm"]
    MIN_LENGTH = 100 
    MAX_PAGES = 500  

    def parse(self, response):
        page_count = response.meta.get('page_count', 1)

        # 1. Get all article links on the current page
        article_links = response.css('ul.blazy li.grid a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, self.parse_article)

        # 2. Handle pagination
        if page_count < self.MAX_PAGES:
            next_page = response.css('ul.pagination li.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, meta={'page_count': page_count + 1}, callback=self.parse)

    def parse_article(self, response):
        paragraphs = response.css('div.field-name-body p::text').getall()
        text = ' '.join([p.strip() for p in paragraphs if p.strip()])

        if text:    
            # Split text by Burmese full stop "။"
            sentences = [s.strip() + "။" for s in text.split("။") if len(s.strip()) >= self.MIN_LENGTH]

            # Group sentences: 1 per item
            for i in range(0, len(sentences), 1):
                chunk = ' '.join(sentences[i:i+1])
                if chunk.strip() and re.search(r"[က-႟]", chunk):  # only yield non-empty chunks
                    item = BurmeseNewsItem()
                    item['text'] = chunk
                    item['category'] = getattr(self, 'category', 'Uncategorized')
                    item['source'] = 'myawady.net.mm'
                    item['url'] = response.url
                    yield item
