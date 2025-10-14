from .base.myawady_base import MyawadyBaseSpider

class MyawadyEducationSpider(MyawadyBaseSpider):
    name = "myawady_education"
    start_urls = [
        "https://www.myawady.net.mm/education"
    ]
    category = "education"
