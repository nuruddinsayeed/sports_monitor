'''
File: auth.py
Project: SportsSafety
File Created: Saturday, 11th June 2022 2:50:19 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Saturday, 11th June 2022 2:50:25 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import MongoClient

from app.settings.configs import get_settings
from app.models.auth_models import Token
from app.models.requests_model import RegisterData
from app.controllers import users
from app.settings import mongo_conf, config_vars


router = APIRouter()
SETTINGS = get_settings()


@router.post("/register", response_model=Token)
async def create_user(register_data: RegisterData,
                      client: MongoClient = Depends(mongo_conf.get_nosql_db)):
    """Register user and return access token"""
    
    db = client.get_database(SETTINGS.spm_mongo_db_name)
    user_colleciton = db.get_collection(config_vars.USER_COLLECTION_NAME)
    
    # create user
    create_info = users.create_user(register_data=register_data, 
                                    collection=user_colleciton)
    
    print(create_info)

    # Login And generate Token
    user = users.authenticate_user(user_mail=register_data.user_email, 
                                   password=register_data.password,
                                   collection=user_colleciton)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token_expire = timedelta(hours=24)
    access_token = users.generate_access_token(
        data={"user_mail": user.user_email},
        expire_delta=token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}