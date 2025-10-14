from .base.mdngov_base import MDNGovBaseSpider

class MDNGovInternationalEducationSpider(MDNGovBaseSpider):
    name = "mdngov_international_education"

    LANGUAGE = "my"

    start_urls = [f"https://www.mdn.gov.mm/{LANGUAGE}/international-education"]
    category = "international-education"
