from pymongo import MongoClient

from app.config.mongo_settings import mongo_settings


class MongoService:
    def __init__(self):
        self.client = MongoClient(
            host=mongo_settings.host,
            port=mongo_settings.port,
        )
        self.db = self.client[mongo_settings.database]

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        collection.insert_one(document)

    def delete_document(self, collection_name, object_query):
        collection = self.db[collection_name]
        collection.delete_one(object_query)

    def update_document(self, collection_name, object_query, update_query):
        collection = self.db[collection_name]
        collection.update_one(object_query, update_query)

    def get_documents(self, collection_name, objects_query):
        collection = self.db[collection_name]
        return collection.find(objects_query)

