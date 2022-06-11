'''
File: __init__.py
Project: SportsSafety
File Created: Friday, 10th June 2022 9:10:50 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Friday, 10th June 2022 9:10:57 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from app.controllers.db_controllers import MongoOperations


def get_mongo_op():
    return MongoOperations()