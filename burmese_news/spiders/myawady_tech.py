import scrapy
from burmese_news.items import BurmeseNewsItem

class MyawadyTechSpider(scrapy.Spider):
    name = "myawady_tech"
    allowed_domains = ["myawady.net.mm"]
    start_urls = [
        "https://www.myawady.net.mm/tech"
    ]

    def parse(self, response):
        # Extract article links
        article_links = response.css('ul.blazy li.grid a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, self.parse_article)

        # Pagination
        next_page = response.css('ul.pagination li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    MIN_LENGTH = 20  # Minimum characters per sentence

    def parse_article(self, response):
        paragraphs = response.css('div.field-name-body p::text').getall()
        text = ' '.join([p.strip() for p in paragraphs if p.strip()])

        if text:
            # Split text by Burmese full stop "။"
            sentences = [s.strip() + "။" for s in text.split("။") if len(s.strip()) >= self.MIN_LENGTH]

            # Group sentences: 1 per item
            for i in range(0, len(sentences), 1):
                chunk = ' '.join(sentences[i:i+1])
                if chunk.strip():  # only yield non-empty chunks
                    item = BurmeseNewsItem()
                    item['text'] = chunk
                    # Set category depending on spider
                    item['category'] = getattr(self, 'category', 'Technology')
                    item['source'] = 'myawady.net.mm'
                    item['url'] = response.url
                    yield item
