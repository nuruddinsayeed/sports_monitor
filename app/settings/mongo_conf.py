'''
File: mongo_conf.py
Project: SportsSafety
File Created: Friday, 10th June 2022 3:48:24 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 10th June 2022 3:48:25 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from pymongo.mongo_client import MongoClient

from app.settings import config_vars
from app.settings.configs import get_settings

SETTINGS = get_settings()


class MongoDB:
    client: MongoClient = None
    
db = MongoDB()

async def connect_to_mongo():
    pass

#TODO: Complete this