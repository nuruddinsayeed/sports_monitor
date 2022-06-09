'''
File: monitor_view.py
Project: SportsSafety
File Created: Friday, 10th June 2022 2:49:13 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 10th June 2022 2:49:16 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from fastapi import APIRouter


router = APIRouter()


@router.get("/home", tags=["Monitor"]) # TODO: add depends
def monitor_home():
    return {"Message": "Hello world"}