# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# https://www.yelp.com/biz/panera-bread-daly-city
class YelpPipeline:

    def parse_about(self, about):
        d = {
            'owner_bio': about.get('businessOwnerBio'),
            'history': about.get('historyText'),
            'specialties': about.get('specialtiesText'),
            'year_est': about.get('yearEstablished')
        }
        return d

    def parse_amenities(self, amenities):
        amenities_cleared = {
                        'amenities': [''.join(elem.get('displayText'))
                                        for properties in amenities.get('organizedProperties')
                                        for elem in properties.get('properties')
                                         ],
                             }
        if amenities.get('healthInspections'):
            amenities_cleared['health'] = {
                'score': amenities.get('healthInspections')[0]['formattedScore'],
                'label': amenities.get('healthInspections')[0]['provider']['displayName']
            }
        return amenities_cleared

    def parse_categories(self, categories):
        categories_cleared = [category for category in categories if isinstance(category, str)]
        return categories_cleared

    def parse_image(self, image_data):
        for data in image_data:
            if not data.get('videoThumbnail'):
                return data.get('srcUrl')

    def process_item(self, item, spider):
        if item.get('about_business'):
            item['about_business'] = self.parse_about(item['about_business'].get('fromTheBusinessContentProps', {}))
        if item.get('amenities'):
            item['amenities'] = self.parse_amenities(item['amenities'])
        if item.get('categories'):
            item['categories'] = self.parse_categories(item['categories'])
        if item.get('main_image'):
            item['main_image'] = self.parse_image(item['main_image'])
        return item
