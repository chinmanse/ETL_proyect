# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from trabajando.utils.functions import convertDate

class TrabajandoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def proccess_array(value):
    print(type(value))
    if isinstance(value, list) and len(value) > 0:
        for elem in value:
            elem = proccess_text(elem)
    return value


def proccess_text(value):
    if isinstance(value, str):
        return value.strip()
    return value
    
def process_date(value):
    return convertDate(value) 

class JobItem(scrapy.Item):
    origin  = scrapy.Field(serializer = proccess_text)
    title  = scrapy.Field(serializer = proccess_text)
    link = scrapy.Field(serializer = proccess_text)
    image = scrapy.Field(serializer = proccess_text)
    resume = scrapy.Field(serializer = proccess_text)
    date_published = scrapy.Field(serializer = process_date)
    author = scrapy.Field(serializer = proccess_text)
    segments = scrapy.Field(serializer = proccess_text)

    def __getitem__(self, key):
        value = super(JobItem, self).__getitem__(key)
        return value
        # """
        # Override __getitem__ to apply serializers when accessing fields
        # This ensures serializers are applied during item access
        # """

        # value = super(JobItem, self).__getitem__(key)
        # field = self.fields[key]

        # if 'serializer' in field:
        #     return field['serializer'](value)

        # return value

