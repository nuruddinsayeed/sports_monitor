'''
File: users.py
Project: SportsSafety
File Created: Friday, 10th June 2022 9:11:26 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 10th June 2022 9:11:30 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.auth_models import UserInDb
from app.settings import mongo_conf


oauth2_shceme = OAuth2PasswordBearer(tokenUrl="token")


def generate_pass_hash(password: str) -> str:
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

def verify_password(password: str, hassed_pass: str | bytes) -> bool:
    return bcrypt.checkpw(password=str(password),
                          hashed_password=str(hassed_pass))
    