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

from app.alerm.activity_waights import ActivityStatus, AlermWeights, WeightCalculator
from app.controllers.db_controllers import MongoOperations
from app.models.activity_models import ActiveUser
from app.settings import config_vars


def get_monitor_mongo_op():
    return MongoOperations(collection_name=config_vars.MONITOR_COLLECTION_NAME)

class AlermController:
    
    def __init__(self, mongo_op: MongoOperations = None,
                 weight_calculator: WeightCalculator=None) -> None:
        self.mongo_op = mongo_op if mongo_op else get_monitor_mongo_op()
        self.weight_calculator = weight_calculator if weight_calculator else \
            WeightCalculator()
    
    def safety_info_from_db(self, username: str) -> ActiveUser:
        # Gets existing safety info from db
        user_curr_info = ActiveUser(
            **self.mongo_op.find_one(filter_data={"username": username}))
        
        # Convert str to ActivityStatus Obj
        user_curr_info.activity_status = ActivityStatus(
            user_curr_info.activity_status)
        return user_curr_info
    
    def update_info_to_db(self, username: str, activity_status: ActivityStatus,
                          activity_weight: int):
        # Update newly measured info to db
        self.mongo_op.update_one(filter_data={"username": username},
                                 update_data={
                                     "activity_status":activity_status,
                                     "activity_weight":activity_weight
                                 })
    
    def is_alerm(self, username: str, new_activity_status: ActivityStatus,
                 new_activity_cls: str):
        # checks if an alerm should be generated
        curr_info = self.safety_info_from_db(username=username)
        
        new_status = self.updated_acivity_status(
            old_status=curr_info.activity_status,
            new_status=new_activity_status
        )
        new_weight = self.updated_weight(curr_weight=int(curr_info.activity_weight),
                                         new_activity_cls=new_activity_cls,
                                         activity_status=new_activity_status)
        
        self.update_info_to_db(username=username, activity_status=new_status, activity_weight=new_weight)
        
        if new_weight > AlermWeights.level_one.value:
            #TODO: trigger alerm
            return True
        return False
        
        
    def updated_acivity_status(self, old_status: ActivityStatus,
                               new_status: ActivityStatus):
        
        critial_activities = (ActivityStatus.dangerous_activity, 
                              ActivityStatus.abnormal_activity,
                              ActivityStatus.disconnected)
        if old_status not in critial_activities or \
            new_status is ActivityStatus.dangerous_activity:
            return new_status
        
        return old_status
    
    def updated_weight(self, curr_weight: int, new_activity_cls: str,
                       activity_status: ActivityStatus):
        new_weight = curr_weight
        
        match new_activity_cls:
            case "sitting":
                new_weight = self.weight_calculator.sitting(curr_w=curr_weight,
                                               activity_status=activity_status)
            case "jogging":
                new_weight = self.weight_calculator.jogging(curr_w=curr_weight)
            case "downstairs":
                new_weight = self.weight_calculator.downstairs(curr_weight)
            case "upstairs":
                new_weight = self.weight_calculator.upstairs(curr_w=curr_weight)
            case "walking":
                new_weight = self.weight_calculator.walking(
                    curr_w=curr_weight, activity_status=activity_status
                )
            case "standing":
                new_weight = self.weight_calculator.standing(
                    curr_w=curr_weight, activity_status=activity_status
                )
            case "disconnected":
                new_weight = self.weight_calculator.disconnected(curr_weight)
            case "abnormal":
                new_weight = self.weight_calculator.abnormal(curr_weight)
            case "fall_detected":
                new_weight = self.weight_calculator.fall_detected(curr_weight)
                
        return new_weight
                