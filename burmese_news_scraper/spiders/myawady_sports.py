from .base.myawady_base import MyawadyBaseSpider

class MyawadySportsSpider(MyawadyBaseSpider):
    name = "myawady_sports"
    start_urls = [
        "https://www.myawady.net.mm/sports"
    ]
    category = "sports"
