'''
File: activity_user_db.py
Project: SportsSafety
File Created: Friday, 17th June 2022 9:33:52 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 17th June 2022 9:35:16 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from datetime import datetime
from typing import List
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import WriteError

from app.models.activity_models import ActiveUser, ActivityInfo, ActivityUserDB
from app.controllers.db_controllers import MongoOperations
from app.settings import config_vars, mongo_conf
from app.settings import mongo_conf
from app.settings.configs import SETTINGS


# def get_activity_collection() -> Collection:
#     db_client = mongo_conf.get_nosql_client()
#     db = db_client.get_database(SETTINGS.spm_mongo_db_name)
#     return db.get_collection(config_vars.ACTIVITY_COLLECTION_NAME)


# def insert_user_activity(user_mdb_id: str, activity_info: ActivityInfo):
#     # create a user info inside user_activity collection
#     collection = get_activity_collection()


#     # generate activity for user
#     user_activity = ActivityUserDB(user_id=user_mdb_id,
#                                    activity_buckets=[activity_info, ])

#     collection.insert_one(user_activity.dict())


# def upload_activity(activity_data: ActivityInfo):
#     collection = get_activity_collection()

#     curr_date_hour = datetime.utcnow().replace(minute=0, second=0,
#                                                microsecond=0)

#     bucket_ob_id = ObjectId()

#     try:
#         collection.update_one(
#             filter={
#                 "user_id": activity_data.user_id,
#                 "activity_buckets.create_at": curr_date_hour
#             },
#             update={
#                 "$push": {
#                     "activity_buckets.$.activities": activity_data.dict()}
#             },
#             upsert=True
#         )
#     except WriteError:
#         collection.insert_one(
#             {"user_id": activity_data.user_id,
#              "activity_buckets": [{"_id": bucket_ob_id,
#                                    "create_at": curr_date_hour,
#                                    "activities": [activity_data.dict(), ]}]}
#         )

def add_active_user(username: str, activity_type:str, mongo_op: MongoOperations):
    user = ActiveUser(username=username, activity_type=activity_type,
                      active_now=True)
    # mongo_op.insert_one(user.dict())
    mongo_op.update_one(filter_data={"username": username},
                        update_data=user.dict(), upsert=True)

def remove_active_user(username: str, mongo_op: MongoOperations):
    # user = ActiveUser(username=username, activity_type=activity_type)
    # mongo_op.delete_many(user.dict())
    mongo_op.update_one(filter_data={"username": username},
                        update_data={"active_now": False})
    
def get_all_active_users(mongo_op: MongoOperations) -> List[ActiveUser]:
    
    all_users = mongo_op.find_many(filter_data={"active_now": True})
    
    return [ActiveUser(**user) for user in all_users]
