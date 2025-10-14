from .base.myawady_base import MyawadyBaseSpider

class MyawadyTechSpider(MyawadyBaseSpider):
    name = "myawady_tech"
    start_urls = [
        "https://www.myawady.net.mm/tech"
    ]
    category = "technology"