from .base.mdngov_base import MDNGovBaseSpider

class MDNGovInternationalEntertainmentSpider(MDNGovBaseSpider):
    name = "mdngov_international_entertainment"

    LANGUAGE = "my"

    start_urls = [f"https://www.mdn.gov.mm/{LANGUAGE}/international-entertainment"]
    category = "international-entertainment"
