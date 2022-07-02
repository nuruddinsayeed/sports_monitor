'''
File: activity.py
Project: SportsSafety
File Created: Sunday, 3rd July 2022 12:19:42 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Sunday, 3rd July 2022 12:19:44 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from fastapi import APIRouter

from app.settings import config_vars
from app.controllers.db_controllers import MongoOperations


router = APIRouter() # /activity


@router.get("/alerms/alerm-count/", name="alerm_count")
async def total_alerm():
    """Count all alerms and return"""
    mongo_op = MongoOperations(
        collection_name=config_vars.MONITOR_COLLECTION_NAME)
    total_alerm = mongo_op.get_document_count(
        filter_data={"alerm_level": { "$gt": 0 }}
    )
    
    return {"alermCount": total_alerm}