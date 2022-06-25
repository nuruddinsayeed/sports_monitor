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

# Alerm will activate in 360
# Stands for 2N (2*3) = 6 min Alerm => 2*3*60 = (360n == 360) -> n=1
# sitting for N (1*3) = 3 min Alerm => 1*3*60 = (180n == 360) -> n=2

class ActivityWeights(Enum):
    alerm_minutes = 3
    standing = 1
    sitting = 2
    disconnected = 360
    abnormal = 360
    fall = 360
    
@unique 
class AlermWeights(Enum):
    level_one = 360
    level_two = 365
    level_three = 370
    level_four = 380
    
class WeightUpdate:
    
    def sitting (curr_w: int) -> int:
        return curr_w + ActivityWeights.sitting.value
    
    def jogging(curr_w: int) -> int:
        return curr_w
    
    def downstairs(curr_w: int) -> int:
        return curr_w
    
    def upstairs(curr_w: int) -> int:
        return curr_w
    
    def upstairs(curr_w: int) -> int:
        return curr_w
    
    def walking(curr_w: int) -> int:
        return curr_w

    def standing(curr_w: int) -> int:
        return curr_w + ActivityWeights.standing.value
    
    def sitting (curr_w: int) -> int:
        return curr_w + ActivityWeights.sitting.value
    
    def disconnected(curr_w: int) -> int:
        return curr_w + ActivityWeights.disconnected.value
    
    def abnormal(curr_w: int) -> int:
        return curr_w + ActivityWeights.abnormal.value
    
    def fall_detected(curr_w: int) -> int:
        return curr_w + ActivityWeights.fall.value
