import pymongo

from scrapy.conf import settings


class ApartmentPipeline(object):
    """Apartment.com pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates apartments table
        """
        connection = pymongo.MongoClient(
                        settings['MONGODB_SERVER'],
                        settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        """
        Save deals in the database.

        This method is called for every item pipement component.
        """
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
            if valid:
                self.collection.insert(dict(item))
                log.msg("Apartment added to MongoDB dataase!",
                        level=log.DEBUG, spider=spider)
        return item
