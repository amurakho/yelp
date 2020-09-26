import scrapy
from scrapy.exceptions import CloseSpider
import json
from yelp.items import YelpItem


class YielpLinkSpiderSpider(scrapy.Spider):
    name = 'yielp_link_spider'
    allowed_domains = ['www.yelp.com']
    start_urls = ['http://www.yelp.com/']

    AMENITIES_URL = 'https://www.yelp.com/gql/batch'
    AMENITIES_DATA = [
        {
            "operationName": "GetBizPageProperties",
            "variables": {"BizEncId": ""},
            "extensions": {"documentId": "f06d155f02e55e7aadb01d6469e34d4bad301f14b6e0eba92a31e635694ebc21"}
        }]

    def __init__(self, **kwargs):
        self.link = None
        super().__init__(**kwargs)

    def start_requests(self):
        if not self.link:
            raise CloseSpider('Have no links')
        else:
            yield scrapy.Request(self.link, callback=self.parse)

    def parse(self, response, **kwargs):
        page_hash_script = response.css('#yelp-js-error-reporting-init-error-reporting::text').get()
        page_hash = json.loads(page_hash_script).get('config', {}).get('release')

        if not page_hash:
            raise CloseSpider('Have no page hash')

        data_key = "yelp_main__{}__yelp_main__BizDetailsApp__dynamic".format(page_hash)

        data_block = response.xpath('//div[@data-hypernova-key="{}"]'.format(data_key))
        main_data = data_block.xpath('script[contains(text(), "telephone")]/text()').get()
        main_data = json.loads(main_data)

        item = YelpItem()

        item['name'] = main_data.get('name')
        item['url'] = response.url
        item['email'] = None
        item['address'] = main_data['address']
        item['rating'] = main_data['aggregateRating']['ratingValue']
        item['reviews_count'] = main_data['aggregateRating']['reviewCount']

        cat_block = response.xpath('//script[@data-hypernova-key="{}"]/text()'.format(data_key)).get()
        cat_data = json.loads(cat_block[4:-3])
        business_id = cat_data['bizDetailsPageProps']['claimStatusGQLProps']['businessId']

        item['id'] = business_id
        item['categories'] = cat_data['gaConfig']['dimensions']['www']['second_level_categories'] + \
                             cat_data['gaConfig']['dimensions']['www']['top_level_categories']
        item['business_website'] = cat_data['bizDetailsPageProps']['bizContactInfoProps'] \
            .get('businessWebsite', {}).get('linkText')
        item['work_schedule'] = cat_data['bizDetailsPageProps']['bizHoursProps']['hoursInfoRows']
        item['about_business'] = cat_data['bizDetailsPageProps']['fromTheBusinessProps']
        # item['about_business'] = cat_data['bizDetailsPageProps'].get('fromTheBusinessProps', {}) \
        #     .get('fromTheBusinessContentProps')
        item['main_image'] = cat_data['bizDetailsPageProps']['photoHeaderProps']['photoHeaderMedias']
        item['phone'] = cat_data['bizDetailsPageProps']['bizContactInfoProps'].get('phoneNumber')

        self.AMENITIES_DATA[0]['variables']['BizEncId'] = business_id
        yield scrapy.http.JsonRequest(self.AMENITIES_URL,
                                      data=self.AMENITIES_DATA,
                                      callback=self.parse_amenities,
                                      method='POST',
                                      meta={'item': item})

    def parse_amenities(self, response):
        item = response.meta.get('item')
        item['amenities'] = response.json()[0]['data']['business']
        return item

