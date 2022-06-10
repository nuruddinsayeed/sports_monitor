'''
File: configs.py
Project: SportsSafety
File Created: Wednesday, 8th June 2022 11:20:13 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Wednesday, 8th June 2022 11:20:15 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

import functools
import logging

from pydantic import BaseSettings, BaseModel

ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]
# CFG_LOGGER = logging.getLogger("app.config")
CFG_LOGGER = logging.getLogger("spm_logger") # SPM for sports Monitoring


class _Settings(BaseSettings):
    """Receive required environment variable from environment or .env file"""

    spm_host: str = "127.0.0.1"
    spm_port: int = 8000
    spm_access_key: str = "MySuperSecretAccessKey"
    jwt_token_algo:str = "HS256"
    spm_secret_key: str = "MySuperSecretApiKey"

    debug: bool = False
    debug_exceptions: bool = False
    
    # Mongo Config
    spm_mongo_db_name="spm_mongo"
    spm_mongo_host:str = "127.0.0.1"
    spm_mongo_port:int = 27017

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@functools.lru_cache()
def get_settings(**kwargs) -> _Settings:

    CFG_LOGGER.info("Loading Config settings from Environment ...")

    return _Settings(**kwargs)


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "spn_logger"
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s [%(thread)d - %(threadName)s] in %(module)s - %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default'
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app/Logs/logs.log',
            'formatter': 'default',
            'maxBytes': 1000000,
            'backupCount': 10,
            "level": LOG_LEVEL,
        }
    }
    loggers = {
        "spm_logger": {
            "handlers": ["default", "logfile"],
            "level": LOG_LEVEL
        },
    }