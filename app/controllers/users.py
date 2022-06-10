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

from typing import Union
import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.auth_models import UserInDb
from app.controllers.db_controllers import MongoOperations


oauth2_shceme = OAuth2PasswordBearer(tokenUrl="token")


def generate_pass_hash(password: str) -> str:
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())

def verify_password(password: str, hassed_pass: str | bytes) -> bool:
    return bcrypt.checkpw(password=str(password),
                          hashed_password=str(hassed_pass))

def get_user(user_mail: str, mongo_op: MongoOperations) -> UserInDb:
    return mongo_op.get_user(user_mail=user_mail)

def create_user(user_name: str, user_email: str, password: str,
                      mongo_op: MongoOperations):
    password_hash = generate_pass_hash(password=password)
    user = UserInDb(username=user_name,
                    user_email=user_email,
                    hashed_password=password_hash,
                    active=True)
    
    return mongo_op.add_user(user_data=user)
    
def authenticate_user(user_mail: str, password: str,
                      mongo_op: MongoOperations = MongoOperations()
                      ) -> Union[bool, UserInDb]:
    user = get_user(user_mail=user_mail, mongo_op=mongo_op)
    
    if not user:
        return False
    
    if not verify_password(password=password, hassed_pass=user.hashed_password):
        return False
    
    return user