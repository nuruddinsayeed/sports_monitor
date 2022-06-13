'''
File: home_view.py
Project: SportsSafety
File Created: Tuesday, 14th June 2022 1:35:44 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Tuesday, 14th June 2022 1:35:46 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter()
templates = Jinja2Templates("app/templates")


# Login Page
@router.get("/login", name="login")
async def index(request: Request):
    """Renders the login page"""

    return templates.TemplateResponse('login.html', {'request': request})


@router.get("/register", name="register")
async def index(request: Request):
    """Renders the register page"""

    return templates.TemplateResponse('register.html', {'request': request})