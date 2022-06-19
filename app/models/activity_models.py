'''
File: activity_models.py
Project: SportsSafety
File Created: Tuesday, 14th June 2022 12:23:21 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Tuesday, 14th June 2022 12:23:30 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class ActivityData(BaseModel):
    x: float
    y: float
    z: float


class ActivityInfo(ActivityData):
    activity_class: str
    user_id: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# class ActivitySingleMDB(ActivityInfo):
#     created_at: datetime = Field(default_factory=datetime.utcnow)


class ActivityBucketMDB(BaseModel):
    _id: ObjectId
    activities: List[ActivityInfo]


class ActivityUserDB(BaseModel):
    _id: ObjectId
    user_id: str
    activity_buckets: List[ActivityBucketMDB]
