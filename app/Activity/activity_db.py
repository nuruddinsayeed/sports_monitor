'''
File: activity_db.py
Project: SportsSafety
File Created: Friday, 17th June 2022 9:33:52 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 17th June 2022 9:35:16 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from tkinter import E
from typing import List
import pymongo
from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import WriteError
from app.controllers import db_controllers
from app.helpers.excepitons import NotFoundError

from app.models.activity_models import ActivityInfo, ActivityUserDB
from app.routes.websockets_route import get
from app.settings import config_vars, mongo_conf
from app.settings import mongo_conf
from app.settings.configs import SETTINGS


def get_activity_collection() -> Collection:
    db_client = mongo_conf.get_nosql_client()
    db = db_client.get_database(SETTINGS.spm_mongo_db_name)
    return db.get_collection(config_vars.ACTIVITY_COLLECTION_NAME)


def insert_user_activity(user_mdb_id: str, activity_info: ActivityInfo):
    # create a user info inside user_activity collection
    collection = get_activity_collection()

    # curr_date_hour = datetime.utcnow().replace(minute=0, microsecond=0)
    # _id = ObjectId().from_datetime(generation_time=curr_date_hour)

    # generate activity for user
    user_activity = ActivityUserDB(user_id=user_mdb_id,
                                   activity_buckets=[activity_info, ])

    collection.insert_one(user_activity.dict())


def upload_activity(activity_data: ActivityInfo):
    collection = get_activity_collection()

    curr_date_hour = datetime.utcnow().replace(minute=0, second=0,
                                               microsecond=0).timestamp()
    # bucket_ob_id = ObjectId().from_datetime(generation_time=curr_date_hour)
    # bucket_ob_id = ObjectId(f'activitybucket-{user_mdb_id}-{round(curr_date_hour.timestamp())}')
    # bucket_ob_id = ObjectId(hex(12545896587458522))
    bucket_ob_id = ObjectId()

    # ret = collection.update_one({"user_id": user_mdb_id },
    #                       {"$push": {"activity_buckets": {**activity_data.dict()}}})

    # collection.insert_one({"user_id": user_mdb_id,"activity_buckets":[{"_id": bucket_ob_id, "create_at":curr_date_hour, "activities": []}] })
    # ret = collection.update_one({"user_id": user_mdb_id, "activity_buckets._id": bucket_ob_id },
    #                     {"$push": {"activity_buckets.$.activities": activity_data.dict()}})

    total_document = collection.count_documents({
                "user_id": activity_data.user_id,
                "activity_buckets.create_at": curr_date_hour
            })
    
    if total_document: # > 0
        collection.update_one(
            filter={
                "user_id": activity_data.user_id,
                "activity_buckets.create_at": curr_date_hour
            },
            update={
                "$push": {
                    "activity_buckets.$.activities": activity_data.dict()}
            }
        )
    else:
        collection.update_one(
            filter={
                "user_id": activity_data.user_id,
            },
            update={
                "$push": {
                    "activity_buckets": {
                        "_id": bucket_ob_id,
                        "create_at": curr_date_hour,
                        "activities": [activity_data.dict(), ]
                    }}
            },
            upsert=True
        )
    
    # try:
    #     collection.update_one(
    #         filter={
    #             "user_id": activity_data.user_id,
    #             "activity_buckets.create_at": curr_date_hour
    #         },
    #         update={
    #             "$push": {
    #                 "activity_buckets.$.activities": activity_data.dict()}
    #         },
    #         upsert=True
    #     )
    # except WriteError as e:
    #     raise e
    #     collection.insert_one(
    #         {"user_id": activity_data.user_id,
    #          "activity_buckets": [{"_id": bucket_ob_id,
    #                                "create_at": curr_date_hour,
    #                                "activities": [activity_data.dict(), ]}]}
    #     )

    # collection.update_one(
    #     filter={
    #         "user_id": user_mdb_id
    #     },
    #     update={
    #         "$push": {
    #             "activity_buckets.$[i].activities": activity_data.dict()}
    #     },
    #     array_filters=[{'i.create_at': curr_date_hour},],
    #     upsert=True
    #     )

    # collection.update_one(
    #     filter={
    #         "user_id": user_mdb_id,
    #     },
    #     update={
    #         "$push": {
    #             "activities": activity_data.dict()}
    #     },
    #     upsert=True
    #     )

    # collection.insert_one({"user_id": user_mdb_id, **activity_data.dict()})

    # find = collection.find_one({"user_id": user_mdb_id, "activity_buckets.create_at": curr_date_hour })
    # print(f'============== {find} id {curr_date_hour}')


def validate_activities(activities: list) -> List[ActivityInfo]:
    return [ActivityInfo(**activity) for activity in activities]

def get_latest_activities(user_id: str) -> List[ActivityInfo]:
    
    """Returns n number of activity of the user"""
    
    collection = get_activity_collection()
    
    pipeline = [
        {
            "$match": {"user_id": user_id},
        },
        {"$unwind": "$activity_buckets"},
        {
            "$sort": {'activity_buckets.create_at': pymongo.DESCENDING},
        },
        {
            "$limit": 1,
        }
    ]
        
    activity_bucket = collection.aggregate(pipeline)
    res: dict = activity_bucket.next()
    
    if not res:
        raise NotFoundError("No User Activity found") 
    
    formated_acivities =  db_controllers.format_mongo_ids(res)
    
    try:
        activities: list = formated_acivities["activity_buckets"]["activities"]
    except KeyError:
        raise NotFoundError("No User Activity found") 
    
    # TODO: Check if this can be done in Mongo query
    activities.sort(key=lambda x: x.get("created_at"))
    validated_activities = validate_activities(activities)
    return validated_activities