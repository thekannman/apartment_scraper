BOT_NAME = 'apartment'

SPIDER_MODULES = ['apartment_app.spiders']
NEWSPIDER_MODULE = 'apartment_app.spiders'

ITEM_PIPELINES = ['apartment_app.pipelines.ApartmentPipeline']

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "apartment"
MONGODB_COLLECTION = "apartments"
