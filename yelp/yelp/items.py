# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    street_address = scrapy.Field()
    address = scrapy.Field()
    postcode_address = scrapy.Field()
    rating = scrapy.Field()
    reviews_count = scrapy.Field()
    categories = scrapy.Field()
    business_website = scrapy.Field()
    work_schedule = scrapy.Field()
    about_business = scrapy.Field()
    amenities = scrapy.Field()
    main_image = scrapy.Field()