from .base.mdngov_base import MDNGovBaseSpider

class MDNGovInternationalSportsSpider(MDNGovBaseSpider):
    name = "mdngov_international_sports"

    LANGUAGE = "my"

    start_urls = [f"https://www.mdn.gov.mm/{LANGUAGE}/international-sports"]
    category = "international-sports"
