from .base.mdngov_base import MDNGovBaseSpider

class MDNGovLocalEntertainmentSpider(MDNGovBaseSpider):
    name = "mdngov_local_entertainment"

    LANGUAGE = "my"

    start_urls = [f"https://www.mdn.gov.mm/{LANGUAGE}/local-entertainment"]
    category = "local-entertainment"
