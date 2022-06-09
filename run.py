'''
File: run.py
Project: SportsSafety
File Created: Wednesday, 8th June 2022 10:22:31 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 10th June 2022 3:29:47 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from distutils.log import debug
from imp import reload
import uvicorn

from app.settings.configs import get_settings

APP_SETTINGS = get_settings()


if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host= APP_SETTINGS.spm_host,
        port=APP_SETTINGS.spm_port,
        log_level="info",
        debug=APP_SETTINGS.debug,
        reload=APP_SETTINGS.debug
    )
