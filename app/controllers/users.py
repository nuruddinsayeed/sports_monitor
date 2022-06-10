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
from typing import Union
from datetime import datetime, timedelta
from jose import JWSError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.settings import configs
from app.models.auth_models import TokenData, User, UserInDb
from app.controllers.db_controllers import MongoOperations


oauth2_shceme = OAuth2PasswordBearer(tokenUrl="token")
SETTINGS = configs.get_settings()


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

def generate_access_token(data: dict, expire_delta: timedelta = None):
    to_encode = data.copy()
    expire = expire_delta if expire_delta \
        else datetime.utcnow() + timedelta(hours=24)
    SECRET_KEY = SETTINGS.spm_secret_key
    ALGORITHM = SETTINGS.jwt_token_algo
    
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_shceme)) -> User:
    
    SECRET_KEY = SETTINGS.spm_secret_key
    ALGORITHM = SETTINGS.jwt_token_algo
    
    err_msg = "Authentication Failed, Please Check you password or email"
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail=err_msg,
                                   headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY,
                             algorithms=[ALGORITHM])
        user_mail = payload.get("user_mail", None)
        token_data = TokenData(user_email=user_mail)
        if not user_mail:
            raise auth_exception
    except JWSError:
        raise auth_exception
    
    user = get_user(user_mail=token_data.user_email)
    
    if not user:
        raise auth_exception
    
    return User(**user)