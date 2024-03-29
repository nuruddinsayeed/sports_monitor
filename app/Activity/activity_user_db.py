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


def add_active_user(username: str, activity_type:str, mongo_op: MongoOperations):
    user = ActiveUser(username=username, activity_type=activity_type,
                      active_now=True)
    user_dict = user.dict()
    
    
    current_info = mongo_op.find_one({"username": username}, exit_silent=True)
    if current_info:
        diff = datetime.utcnow() - datetime.strptime(
            current_info.get("last_update"), '%d/%m/%Y %H:%M:%S'
        )
        diff_hr = diff.total_seconds() / 3600
        if diff_hr < 2: # user was connected 2 hour ago
            # dont reset
            user_dict.pop("activity_weight", None)
            
        
    
    mongo_op.update_one(filter_data={"username": username},
                        update_data=user_dict, upsert=True)

def remove_active_user(username: str, mongo_op: MongoOperations):
    # user = ActiveUser(username=username, activity_type=activity_type)
    # mongo_op.delete_many(user.dict())
    data = {
        "active_now": False,
        "last_update": datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')
    }
    mongo_op.update_one(filter_data={"username": username},
                        update_data=data)
    
def get_all_active_users(mongo_op: MongoOperations) -> List[ActiveUser]:
    
    all_users = mongo_op.find_many(filter_data={"active_now": True})
    
    return [ActiveUser(**user) for user in all_users]

def get_all_alermed_users(mongo_op: MongoOperations) -> List[ActiveUser]:
    alermed_users = mongo_op.find_many(
        filter_data={ "activity_weight": { "$gt": 359 } }
    )
    
    return [ActiveUser(**user) for user in alermed_users]
