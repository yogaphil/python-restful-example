from bson.objectid import ObjectId
from pymongo import MongoClient


class MongoService:

    def __init__(self, config_dict: dict):
        self.mongo_url = config_dict["MONGODB_URL"]
        self.mongo_db_name = config_dict["MONGO_DB_NAME"]
        if self.mongo_url is None:
            raise ValueError("Did not find MONGODB_URL in the configuration dict.")
        self.client = MongoClient(self.mongo_url)

    def get_collection_for_resource(self, resource_name):
        db = self.client.get_database(self.mongo_db_name)
        res_collection = db.get_collection(resource_name)
        #        if len(res_collection.index_information()) == 1:
        #            res_collection.create_index([("{n}_id".format(n=resource_name), ASCENDING)], unique=True)
        return res_collection

    def get_resource_by_id(self, resource_name: str, resource_id: str):
        res_collection = self.get_collection_for_resource(resource_name)
        query = {"_id": ObjectId(resource_id)}
        return res_collection.find_one(query)

    def save_resource(self, resource_name: str, resource_data):
        res_collection = self.get_collection_for_resource(resource_name)
        result = res_collection.insert_one(resource_data)
        return result.inserted_id

    def get_all_resource_of_type(self, resource_name: str):
        res_collection = self.get_collection_for_resource(resource_name)
        return res_collection.find()
