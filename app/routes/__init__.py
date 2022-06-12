'''
File: __init__.py
Project: SportsSafety
File Created: Wednesday, 8th June 2022 10:56:28 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Wednesday, 8th June 2022 10:56:30 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from fastapi import APIRouter

from .monitor_view import router as monitor_router
from .websockets import router as ws_router

router = APIRouter()
router.include_router(monitor_router, prefix="/monitor-admin", tags=["monitor"])
router.include_router(ws_router, prefix="/ws")
