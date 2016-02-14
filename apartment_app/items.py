from scrapy.item import Item, Field


class ApartmentListing(Item):
    """Apartment.com container (dictionary-like object) for scraped data"""
    name = Field()
    beds = Field()
    baths = Field()
    sqft_min = Field()
    sqft_max = Field()
    price_min = Field()
    price_max = Field()
    address = Field()

