import scrapy
from burmese_news.items import BurmeseNewsItem

class MDNGovLocalEducationSpider(scrapy.Spider):
    name = "mdngov_local_education"
    allowed_domains = ["mdn.gov.mm"]
    start_urls = ["https://www.mdn.gov.mm/my/local-education"]

    MAX_LENGTH = 50

    def start_requests(self):
        """Use Playwright to render the page fully"""
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                },
                callback=self.parse
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        try:
            # Wait for content to load
            await page.wait_for_selector("div.item", timeout=10000)
            content = await page.content()
            
            selector = scrapy.Selector(text=content)
            
            # Extract article links
            articles = selector.css("div.item")
            self.logger.info(f"Found {len(articles)} articles on page")
            
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
        except Exception as e:
            self.logger.error(f"Error parsing main page: {e}")
        finally:
            await page.close()

    async def parse_article(self, response):
        page = response.meta["playwright_page"]
        
        try:
            # Wait for the main article content (not the footer)
            await page.wait_for_selector("article.node--type-article", timeout=10000)
            content = await page.content()
            
            selector = scrapy.Selector(text=content)
            
            # Extract article text - MORE SPECIFIC SELECTORS to avoid footer
            paragraphs = []
            
            # Try these specific selectors for article content (avoid footer)
            content_selectors = [
                "article.node--type-article div.field--name-body p::text",
                "article.node--type-article div.field--name-body ::text",
                "div.field--name-body:not(footer *) p::text",  # Exclude footer
                "article p::text",
                ".node__content .field--name-body p::text",
                "div.field--name-body p::text",
                # If above don't work, try to exclude footer explicitly
                "p:not(footer p)::text",
                "div:not(footer) p::text"
            ]
            
            for selector_pattern in content_selectors:
                found_paragraphs = selector.css(selector_pattern).getall()
                if found_paragraphs:
                    # Filter out copyright/footer text
                    filtered_paragraphs = [
                        p.strip() for p in found_paragraphs 
                        if p.strip() 
                        and "copyright" not in p.lower() 
                        and "©" not in p
                        and len(p.strip()) > 20  # Minimum length to avoid short fragments
                    ]
                    if filtered_paragraphs:
                        paragraphs = filtered_paragraphs
                        self.logger.info(f"Found {len(paragraphs)} paragraphs using: {selector_pattern}")
                        self.logger.info(f"First paragraph sample: {paragraphs[0][:100]}...")
                        break
            
            full_text = " ".join(paragraphs)
            
            self.logger.info(f"Content length: {len(full_text)}")
            
            if full_text and len(full_text) > 50:  # Only yield if we have substantial content
                # Process text into chunks
                sentences = [s.strip() + "။" for s in full_text.split("။") if len(s.strip()) > 10]
                
                if sentences:
                    for i in range(0, len(sentences)):
                        chunk = sentences[i]
                        if len(chunk) >= self.MAX_LENGTH:
                            item = BurmeseNewsItem()
                            item["text"] = chunk
                            item["category"] = "Local Education"
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