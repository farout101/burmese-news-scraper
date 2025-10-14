from .base.mdngov_base import MDNGovBaseSpider

class MDNGovInternationalPoliticalSpider(MDNGovBaseSpider):
    name = "mdngov_international_political"

    LANGUAGE = "my"

    start_urls = [f"https://www.mdn.gov.mm/{LANGUAGE}/international-political"]
    category = "international-political"
