'''
File: auth_models.py
Project: SportsSafety
File Created: Friday, 10th June 2022 8:52:04 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 10th June 2022 8:52:07 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class User(BaseModel):
    username: str
    user_email: str
    hashed_password: str
    active: bool = True
    
class UserInDb(User):
    _id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None