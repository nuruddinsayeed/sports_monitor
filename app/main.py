'''
File: main.py
Project: SportsSafety
File Created: Wednesday, 8th June 2022 10:39:26 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Wednesday, 8th June 2022 10:54:29 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

import logging
from logging.config import dictConfig
from app import app_version
from app.settings.configs import get_settings, ALLOWED_ORIGINS, LogConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.helpers import file_helper

logger = logging.getLogger('sps_logger')
settings = get_settings()

# ############
# FastAPI App
# ############

def get_app() -> FastAPI:
    """Returns fastapi app"""
    
    app = FastAPI(
        title="Long Distance Sports Safety",
        description="Detection of Human activity for Emergency Response in\
            long-distance Sports using smartwatch/wearable sensors/smartphones",
        version= app_version,
        debug=settings.debug
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"] #TODO: Change it
    )
    
    app.mount("/app/static/", StaticFiles)
    
    return app

def configure_routes(app: FastAPI) -> None:
    """Configure all routes"""
    # from app.routes import home_router

    # app.include_router(home_router, prefix="", tags=["home"])
    pass


# initialize app
app = get_app()

@app.on_event('startup')
async def startup_event():
    """Startup events that need to start at the start of the app"""
    
    # Configure Logging
    file_helper.create_log_dir()
    dictConfig(LogConfig().dict())
    
    logger.info("Hiii, I am 'SP Monitor'. I just started Running :)")
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("Hyyy Human!!! I Stopped Runnig :'(!! Can you pelase help\
        me to run again")

configure_routes(app=app)