'''
File: requests_model.py
Project: SportsSafety
File Created: Saturday, 11th June 2022 2:55:34 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Saturday, 11th June 2022 2:55:37 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from pydantic import BaseModel

class RegisterData(BaseModel):
    username: str
    user_email: str
    password: str