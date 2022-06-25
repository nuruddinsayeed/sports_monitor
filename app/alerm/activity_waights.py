'''
File: activity_waights.py
Project: SportsSafety
File Created: Saturday, 25th June 2022 4:16:25 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Saturday, 25th June 2022 4:16:28 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

from enum import Enum, unique

from app.helpers.excepitons import Invalid

# Alerm will activate in 360
# Stands for 2N (2*3) = 6 min Alerm => 2*3*60 = (360n == 360) -> n=1
# sitting for N (1*3) = 3 min Alerm => 1*3*60 = (180n == 360) -> n=2

class ActivityWeights(Enum):
    alerm_minutes = 3
    standing = 1
    sitting = 2
    disconnected = 360
    abnormal = 360
    fall = 361
    
@unique 
class AlermWeights(Enum):
    level_one = 360
    level_two = 365
    level_three = 370
    level_four = 400
    
class ActivityStatus(Enum):
    normal_activity = "Normal Activity"
    abnormal_activity = "Abnormal Activity"
    dangerous_activity = "Dangerous Activity"
    
class WeightUpdate:
    
    def sitting (curr_w: int, activity_status: ActivityStatus) -> int:
        
        if activity_status is ActivityStatus.normal_activity:
            return curr_w + ActivityWeights.sitting.value
        if activity_status is ActivityStatus.abnormal_activity:
            return AlermWeights.level_three.value
        if activity_status is ActivityStatus.dangerous_activity:
            return AlermWeights.level_four.value
        
        raise Invalid(f"Invalid Activity Status {activity_status}")
        
    
    def jogging(curr_w: int) -> int:
        return curr_w
    
    def downstairs(curr_w: int) -> int:
        return curr_w
    
    def upstairs(curr_w: int) -> int:
        return curr_w
    
    def walking(curr_w: int, activity_status: ActivityStatus) -> int:
        if activity_status is ActivityStatus.normal_activity:
            return curr_w
        if activity_status is ActivityStatus.abnormal_activity:
            return AlermWeights.level_three.value
        if activity_status is ActivityStatus.dangerous_activity:
            return AlermWeights.level_four.value
        
        raise Invalid(f"Invalid Activity Status {activity_status}")

    def standing(curr_w: int, activity_status: ActivityStatus) -> int:
        if activity_status is ActivityStatus.normal_activity:
            return curr_w + ActivityWeights.standing.value
        if activity_status is ActivityStatus.abnormal_activity:
            return AlermWeights.level_three.value
        if activity_status is ActivityStatus.dangerous_activity:
            return AlermWeights.level_four.value
        
        raise Invalid(f"Invalid Activity Status {activity_status}")
    
    def disconnected(curr_w: int) -> int:
        return curr_w + ActivityWeights.disconnected.value
    
    def abnormal(curr_w: int) -> int:
        return curr_w + ActivityWeights.abnormal.value
    
    def fall_detected(curr_w: int) -> int:
        return curr_w + ActivityWeights.fall.value
