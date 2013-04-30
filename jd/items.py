# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class Employee(Item):
    uid = Field()
    preferred_name = Field()
    photo_url = Field()
    phone = Field()
    extension = Field()
    mobile = Field()
    email = Field()
    cube = Field()
    manager = Field()
    department = Field()
    address = Field()
