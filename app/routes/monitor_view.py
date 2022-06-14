'''
File: monitor_view.py
Project: SportsSafety
File Created: Friday, 10th June 2022 2:49:13 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Tuesday, 14th June 2022 1:39:39 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''


from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter()
templates = Jinja2Templates("app/templates")


# @router.get("/") # TODO: add depends
# def monitor_home():
#     return {"Message": "Hello world"}

# Activity Monitor Page
@router.get("/", name="monitor",)
async def index(request: Request):
    """Renders the login page"""

    return templates.TemplateResponse('monitor_view.html', {'request': request})

@router.get("/activity-detail", name="activity_detail",)
async def index(request: Request):
    """Renders the login page"""

    return templates.TemplateResponse('activity_view.html', {'request': request})