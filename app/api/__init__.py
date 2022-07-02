'''
File: __init__.py
Project: SportsSafety
File Created: Wednesday, 8th June 2022 10:38:58 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Wednesday, 8th June 2022 10:55:04 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from fastapi import APIRouter
from .auth import router as auth_router
from .activity import router as activity_router


router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth", "api"])
router.include_router(activity_router, prefix="/activity",
                      tags=["activity", "api"])
