'''
File: db_controllers.py
Project: SportsSafety
File Created: Friday, 10th June 2022 9:43:38 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 10th June 2022 9:43:39 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from turtle import update
from typing import List
from app.helpers.excepitons import NotFoundError
from app.models.activity_models import ActiveUser
from app.models.auth_models import UserInDb
from app.settings import config_vars, configs
from app.settings.mongo_conf import get_nosql_client

SETTINGS = configs.get_settings()


def format_mongo_ids(nested_dicts: dict, exit_silent: bool = False):
    """
    Loops through nested dictionary (with arrays 1 layer deep) to
    properly format the MongoDB '_id' field to a string instead of an ObjectId
    """
    
    if not nested_dicts:
        if exit_silent:
            return None
        raise NotFoundError("Data not found!!")
    
    for key, val in nested_dicts.items():
        if isinstance(val, dict):
            nested_dicts[key] = format_mongo_ids(val)
        elif isinstance(val, list):
            new_arr = []
            for item in val:
                if isinstance(item, dict):
                    new_arr.append(format_mongo_ids(item))
                else:
                    new_arr.append(item)
            nested_dicts[key] = new_arr
        elif key == "_id":
            nested_dicts[key] = str(val)

    return nested_dicts


class MongoOperations:

    def __init__(self, collection_name: str,
                 db_name: str = SETTINGS.spm_mongo_db_name) -> None:
        self.db = get_nosql_client()[db_name]
        self.collection = self.db.get_collection(collection_name)

    # def get_user_collection(self):
    #     return self.db.get_collection(config_vars.USER_COLLECTION_NAME)

    def insert_one(self, data: dict):
        self.collection.insert_one(data)

    def update_one(self, filter_data: dict, update_data: dict, upsert: bool = True):
        self.collection.update_one(filter=filter_data,
                                   update={"$set": update_data}, upsert=upsert)

    def delete_one(self, filter_data: dict):
        self.collection.delete_one(filter=filter_data)

    def delete_many(self, filter_data: dict):
        self.collection.delete_many(filter=filter_data)

    def insert_many(self, data: List[dict]):
        self.collection.insert_many(data)

    # def find_all(self):
    #     all_documents = self.collection.find({})
    #     return format_mongo_ids(all_documents)

    def find_one(self, filter_data: dict, exit_silent: bool = True):
        one_document = self.collection.find_one(filter=filter_data)
        return format_mongo_ids(nested_dicts=one_document,
                                exit_silent=exit_silent)

    def find_many(self, filter_data: dict):
        all_docs = self.collection.find(filter_data)
        all_docs = [format_mongo_ids(doc) for doc in all_docs]
        return all_docs