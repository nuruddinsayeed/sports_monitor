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
import logging
from pymongo.mongo_client import MongoClient

from app.settings import config_vars
from app.settings.configs import get_settings

SETTINGS = get_settings()
SPM_LOGGER = logging.getLogger("spm_logger")

class MongoDB:
    client: MongoClient = None
    
db = MongoDB()

async def connect_to_mongo():
    host = SETTINGS.spm_mongo_host
    port = SETTINGS.spm_mongo_port
    db.client = MongoClient(f"mongodb://{host}:{port}/", 
                            maxPoolSize=config_vars.MAX_CONNECTIONS_COUNT, 
                            minPoolSize=config_vars.MIN_CONNECTIONS_COUNT)
    SPM_LOGGER.info("MongoDb Connected")
    
async def disconnect_mongo():
    db.client.close()
    SPM_LOGGER.info("MongoDB Disconnected")
    
async def get_nosql_db() -> MongoClient:
    return db.client
