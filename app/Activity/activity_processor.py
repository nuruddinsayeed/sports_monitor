'''
File: activity_processor.py
Project: SportsSafety
File Created: Tuesday, 14th June 2022 12:58:51 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Tuesday, 14th June 2022 12:59:01 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''
import json
import logging
from json.decoder import JSONDecodeError
from pydantic.error_wrappers import ValidationError

from app.helpers.excepitons import WrongDataTypeErr
from app.models.activity_models import ActivityInfo
from app.controllers import activity_controller


def validate_data(username: str, data: str) -> ActivityInfo:
    try:
        data = json.loads(data)
        valideted_activity_data = ActivityInfo(**data)
    except (JSONDecodeError, ValidationError) as e:
        raise WrongDataTypeErr("Data must be like x:1, y:2, z:3 json") # TODO: Change this
    
    # add user name and jsonify
    valideted_activity_data.username = username
    
    return valideted_activity_data

def process_activity(username: str, activity_type: str,
                     data: str) -> str:
    
    # validate dataq
    validated_data = validate_data(username=username, data=data)
    db_data = ActivityInfo(**validated_data.dict())
    
    # store to mongoDB
    activity_controller.upload_activity(user_mdb_id=username,
                                        activity_data=db_data)
    
    json_data = json.dumps(validated_data.dict(), default=str)
    print(validated_data, username, activity_type)
    
    return json_data