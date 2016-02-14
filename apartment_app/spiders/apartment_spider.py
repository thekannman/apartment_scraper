from scrapy import Spider, Request
from scrapy.selector import Selector
from datetime import datetime
from apartment_app.items import ApartmentListing
import re


class ApartmentSpider(Spider):
    """Spider for regularly updated apartment.com site"""
    name = "apartment"
    allowed_domains = ["apartments.com"]
    start_urls = ["http://www.apartments.com/chicago-il-60606/"]

    apartments_list_xpath = '//article'
    availability_list_xpath = '//*[starts-with(@class,"rentalGridRow")]'
    property_name_xpath = '//*[@class="propertyName"]/h1/text()'
    property_address_xpath = '//*[@itemprop="streetAddress"]/text()'


    def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        Testing contracts:
        @url http://www.apartments.com/chicago-il-60606/
        @returns items 1
        @scrapes title link
        """

        properties = Selector(response).xpath(self.apartments_list_xpath)
        # iterate over properties
        for property in properties:
            url = property.xpath('./@data-url').extract()[0]
            request = Request(url, callback=self.parse_property)
       	    yield request
        AIzaSyB9H0wY0_S6WJEvW0wBQDgozcJXyTrhrGc

    def parse_property(self, response):
        """
        Callback used by Scrapy to process single apartment listing

        Testing contracts:
        @returns items 1
        @scrapes title link
        """
        property_name = Selector(response).xpath(self.property_name_xpath).extract()[0]
        property_address =Selector(response).xpath(self.property_address_xpath).extract()[0]

        apartments = Selector(response).xpath(self.availability_list_xpath)
        for apartment in apartments:
            item = ApartmentListing()
            item['beds'] = int(apartment.xpath('./@data-beds').extract()[0])
            item['baths'] = int(apartment.xpath('./@data-baths').extract()[0])
            non_decimal = re.compile(r'[^\d.]+')
            price = apartment.xpath('./td[@class="rent"]/text()').extract()[0]
            price = price.strip()
            if price[0]=='$':
                price = [non_decimal.sub('', x) for x in price.split('-')]
                item['price_min'] = int(price[0])
                item['price_max'] = int(price[0]) if len(price) == 1 else int(price[1])
            sqft = apartment.xpath('./td[@class="sqft"]/text()').extract()[0]
            sqft = [non_decimal.sub('', x) for x in sqft.split('-')]
            item['sqft_min'] = int(sqft[0])
            item['sqft_max'] = int(sqft[0]) if len(sqft) == 1 else int(sqft[1])
            item['name'] = property_name
            item['address'] = property_address
            yield item
