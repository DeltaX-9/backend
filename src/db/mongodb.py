import pymongo
import logging
import os

class MongoDB:
    def __init__(self, db_name: str, collection_name: str):
        self.client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        

    def connection_status(self):
        logging.info("MongoDB Connection Status: {}".format(self.client is not None))
        return self.client is not None

    def insert(self, data: dict):
        self.collection.insert_one(data)

    def find(self, query: dict):
        return self.collection.find(query)

    def find_one(self, query: dict):
        return self.collection.find_one(query)

    def update(self, query: dict, data: dict):
        self.collection.update_one(query, {"$set": data})

    def delete(self, query: dict):
        self.collection.delete_one(query)