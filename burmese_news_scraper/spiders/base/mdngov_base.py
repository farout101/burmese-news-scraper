import re
import scrapy
from burmese_news_scraper.items import BurmeseNewsItem

class MDNGovBaseSpider(scrapy.Spider):
    allowed_domains = ["mdn.gov.mm"]
    MAX_LENGTH = 100
    MAX_PAGES = 500

    # def start_requests(self):
    #     """Use Playwright to render the page fully"""
    #     for url in self.start_urls:
    #         yield scrapy.Request(
    #             url,
    #             meta={
    #                 "playwright": True,
    #                 "playwright_include_page": True,
    #             },
    #             callback=self.parse
    #         )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        try:
            # Wait for both content AND pagination to load
            await page.wait_for_selector("div.card.mb-3.shadow", timeout=10000)
            await page.wait_for_selector("nav.pager", timeout=5000)  # Wait for pagination too
            content = await page.content()
            
            selector = scrapy.Selector(text=content)
            
            # FIX: Use correct selector for articles
            articles = selector.css("div.view-content-wrap div.item")
            # OR alternative: articles = selector.css("div.card.mb-3.shadow")
            
            self.logger.info(f"Found {len(articles)} articles on page {response.url}")
            
            for article in articles:
                link = article.css("h5.card-title a::attr(href)").get()
                if link:
                    full_url = response.urljoin(link)
                    self.logger.info(f"Found article link: {full_url}")
                    
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.parse_article,
                        meta={
                            "playwright": True,
                            "playwright_include_page": True,
                        },
                    )
            
            # PAGINATION: Debug what we're finding
            next_page_selector = selector.css('li.pager__item--next a::attr(href)').get()
            self.logger.info(f"DEBUG - Next page selector found: {next_page_selector}")
            
            next_page_url = self.get_next_page_url(selector, response)
            self.logger.info(f"DEBUG - Next page URL: {next_page_url}")
            
            if next_page_url:
                self.logger.info(f"Following next page: {next_page_url}")
                yield scrapy.Request(
                    url=next_page_url,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                    },
                    callback=self.parse
                )
            else:
                self.logger.info("No next page found - stopping pagination")
                
        except Exception as e:
            self.logger.error(f"Error parsing main page {response.url}: {e}")
        finally:
            await page.close()

    def get_next_page_url(self, selector, response):
        """Extract the next page URL from pagination"""
        # Try multiple selectors to be safe
        next_page = selector.css('li.pager__item--next a::attr(href)').get()
        if not next_page:
            next_page = selector.css('a[rel="next"]::attr(href)').get()
        if not next_page:
            # Try to find any next page link
            next_page = selector.css('nav.pager a::attr(href)').get()
            
        if next_page:
            full_url = response.urljoin(next_page)
            self.logger.info(f"Next page URL generated: {full_url}")
            return full_url
        return None

    async def parse_article(self, response):
        # Your existing parse_article method is fine
        page = response.meta["playwright_page"]
        
        try:
            await page.wait_for_selector("article.node--type-article", timeout=10000)
            content = await page.content()
            
            selector = scrapy.Selector(text=content)
            
            paragraphs = []
            content_selectors = [
                "article.node--type-article div.field--name-body p::text",
                "article.node--type-article div.field--name-body ::text",
                "div.field--name-body:not(footer *) p::text",
                "article p::text",
                ".node__content .field--name-body p::text",
                "div.field--name-body p::text",
                "p:not(footer p)::text",
                "div:not(footer) p::text"
            ]
            
            for selector_pattern in content_selectors:
                found_paragraphs = selector.css(selector_pattern).getall()
                if found_paragraphs:
                    filtered_paragraphs = [
                        p.strip() for p in found_paragraphs 
                        if p.strip() 
                        and "copyright" not in p.lower() 
                        and "©" not in p
                        and len(p.strip()) > 20
                    ]
                    if filtered_paragraphs:
                        paragraphs = filtered_paragraphs
                        self.logger.info(f"Found {len(paragraphs)} paragraphs using: {selector_pattern}")
                        break
            
            full_text = " ".join(paragraphs)
            self.logger.info(f"Content length: {len(full_text)}")
            
            if full_text and len(full_text) > 100:
                sentences = [s.strip() + "။" for s in full_text.split("။") if len(s.strip()) > 10]
                
                if sentences:
                    for i in range(0, len(sentences)):
                        chunk = sentences[i]
                        if len(chunk) >= self.MAX_LENGTH and re.search(r"[က-႟]", chunk):
                            item = BurmeseNewsItem()
                            item["text"] = chunk
                            item["category"] = getattr(self, 'category', 'Uncategorized')
                            item["source"] = "mdn.gov.mm"
                            item["url"] = response.url
                            yield item
                            self.logger.info(f"Yielded item with {len(chunk)} characters")
                else:
                    self.logger.warning(f"No valid sentences found for article: {response.url}")
            else:
                self.logger.warning(f"No substantial content found for article: {response.url}")
                
        except Exception as e:
            self.logger.error(f"Error parsing article {response.url}: {e}")
        finally:
            await page.close()