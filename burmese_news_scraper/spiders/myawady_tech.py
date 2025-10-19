from .base.myawady_base import MyawadyBaseSpider
import scrapy
class MyawadyTechSpider(MyawadyBaseSpider):
    name = "myawady_tech"
    start_urls = [
        "https://www.myawady.net.mm/tech"
    ]
    category = "technology"
    
    START_PAGE = 20 

    def start_requests(self):
        """Start from a custom page if specified."""
        for url in self.start_urls:
            if self.START_PAGE > 1:
                # Append ?page=N or &page=N depending on URL structure
                connector = "&" if "?" in url else "?"
                url = f"{url}{connector}page={self.START_PAGE}"
            yield scrapy.Request(url, meta={'page_count': self.START_PAGE}, callback=self.parse)