from .base.mdngov_base import MDNGovBaseSpider
import scrapy
class MDNGovInternationalEducationSpider(MDNGovBaseSpider):
    name = "mdngov_international_education"
    LANGUAGE = "my"
    category = "international-education"

    start_urls = [f"https://www.mdn.gov.mm/{LANGUAGE}/{category}"]

    START_PAGE = 5  # Change this number to control where to start

    def start_requests(self):
        """Start from a custom page without changing base spider logic."""
        for url in self.start_urls:
            if self.START_PAGE > 0:
                # If the site uses ?page=N format
                url = f"{url}?page={self.START_PAGE}"
            yield scrapy.Request(
                url,
                meta={"playwright": True, "playwright_include_page": True},
                callback=self.parse,
            )