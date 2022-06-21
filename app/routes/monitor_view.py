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


from fastapi import APIRouter, HTTPException, status
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from app.Activity import activity_db

from app.Activity import activity_db
from app.controllers import auth_control

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

@router.get("/activity-detail/{username}", name="activity_detail",)
async def index(request: Request, username: str):
    """Renders the login page"""
    
    user = auth_control.verify_username(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
        
    activities = activity_db.get_latest_activities(user_id=user.id)
    x, y, z = [], [], []
    for activity in activities[-180:]:
        x.append(activity.x)
        y.append(activity.y)
        z.append(activity.z)
    if len(x) < 180:
        empty_vals = [0 for _ in range(180-len(x))]
        x = [*empty_vals, *x]
        y = [*empty_vals, *y]
        z = [*empty_vals, *z]
    print(x[-10:])

    data = {'request': request, 
            'username': user.username,
            "graph_labels": [i for i in range(180)],
            "accumulator_data_x": x,
            "accumulator_data_y": y,
            "accumulator_data_z": z,}
    return templates.TemplateResponse('activity_view.html', data)

# Active Users Page
# @router.get("/active-users", name="active-users",)
# async def index(request: Request):
#     """Renders the login page""" TODO Complete this

#     return templates.TemplateResponse('monitor_view.html', {'request': request})