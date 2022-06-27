'''
File: safety_measure.py
Project: SportsSafety
File Created: Monday, 27th June 2022 12:32:23 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Monday, 27th June 2022 12:32:25 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from app.alerm.activity_waights import ActivityStatus
from app.controllers.db_controllers import MongoOperations
from app.settings import config_vars


def get_monitor_mongo_op():
    return MongoOperations(collection_name=config_vars.MONITOR_COLLECTION_NAME)

class AlermController:
    
    def __init__(self, mongo_op: MongoOperations = None) -> None:
        self.mongo_op = mongo_op if mongo_op else get_monitor_mongo_op()
    
    def safety_info_from_db(self, username: str):
        # Gets existing safety info from db
        return self.mongo_op.find_one(filter_data={"username": username})
    
    def update_info_to_db(self, username: str, activity_status: ActivityStatus,
                          activity_weight: int):
        # Update newly measured info to db
        self.mongo_op.update_one(filter_data={"username": username},
                                 update_data={
                                     "activity_status":activity_status,
                                     "activity_weight":activity_weight
                                 })
    
    def is_alerm():
        # checks if an alerm should be generated
        # TODO: calculate weights and return if alerm
        pass
    
    # def tes():
    #     srting = "h"
    #     match srting:
    #         case "h":
    #             print("hello world")
    #         case "hello":
    #             print("helowwww worlddd!")
                