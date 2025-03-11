import redis
from django.conf import settings
from django.core.management import call_command
from django.test.runner import DiscoverRunner
from pymongo import MongoClient


class GISDataTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        setup = super().setup_databases(**kwargs)
        call_command("load_gis_data")
        return setup
    
    def teardown_databases(self, *args, **kwargs):
        self.clear_redis()
        self.clear_mongo()
        super().teardown_databases(*args, **kwargs)

    def clear_redis(self):
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        redis_client.flushdb()

    def clear_mongo(self):
        mongo_client = MongoClient(settings.MONGO_URI)
        mongo_client.drop_database('test')