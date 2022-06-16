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
from app.models.activity_models import ActivityData, ActivityInfo


def process_activity(username: str, activity_type: str, data: str):
    try:
        data = json.loads(data)
        activity_data = ActivityInfo(**data)
    except (JSONDecodeError, ValidationError) as e:
        raise WrongDataTypeErr("Data must be like x:1, y:2, z:3 json")
    print(activity_data, username, activity_type)