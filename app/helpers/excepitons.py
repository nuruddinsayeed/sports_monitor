'''
File: excepitons.py
Project: SportsSafety
File Created: Tuesday, 14th June 2022 12:21:44 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Tuesday, 14th June 2022 12:22:18 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''


class WrongDataTypeErr(Exception):
    """Custom Exception for not implementing some methods"""

    def __init__(self, message: str) -> None:
        err = f"Data Is Not valid. {message}"
        super().__init__(err)
        
class NotFoundError(Exception):
    """Custom Exception for when data is not found"""

    def __init__(self, message: str) -> None:
        err = f"Not Found. {message}"
        super().__init__(err)