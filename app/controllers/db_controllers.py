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

from app.models.auth_models import UserInDb
from app.settings.configs import get_settings
from app.settings.mongo_conf import get_nosql_db

SETTINGS = get_settings()

def format_mongo_ids(nested_dicts: dict):
    """
    Loops through nested dictionary (with arrays 1 layer deep) to
    properly format the MongoDB '_id' field to a string instead of an ObjectId
    """
    
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
    async def __init__(self, db_name: str = SETTINGS.spm_mongo_db_name) -> None:
        self.db = await get_nosql_db()[db_name]
        
        
    def get_user(self, user_mail: str) -> UserInDb:
        collection = self.db.users
        row_data = collection.find_one({"user_email": user_mail})
        
        if row_data is not None:
            return format_mongo_ids(row_data)
        return None
    
    def add_user(self, user_data: UserInDb):
        collection = self.db.users
        try:
            response = collection.insert_one(user_data.dict())
            return {"id_inserted": str(response.inserted_id)}
        except Exception as e:
            raise Exception(f"{e}")