from .base.mdngov_base import MDNGovBaseSpider

class MDNGovLocalEducationSpider(MDNGovBaseSpider):
    name = "mdngov_local_education"

    LANGUAGE = "my"

    start_urls = [f"https://www.mdn.gov.mm/{LANGUAGE}/local-education"]
    category = "local-education"
