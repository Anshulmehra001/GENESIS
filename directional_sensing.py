"""
Directional Sensing Module
Organisms have facing direction and vision cones
"""

import math
import random

class DirectionalSensing:
    """Mixin for organisms with directional sensing"""
    
    def __init__(self):
        self.direction = random.randint(0, 7)  # 8 directions (0-7)
        self.vision_cone_angle = 90  # degrees
    
    def get_direction_vector(self):
        """Get dx, dy for current direction"""
        directions = [
            (0, -1),   # 0: North
            (1, -1),   # 1: NE
            (1, 0),    # 2: East
            (1, 1),    # 3: SE
            (0, 1),    # 4: South
            (-1, 1),   # 5: SW
            (-1, 0),   # 6: West
            (-1, -1)   # 7: NW
        ]
        return directions[self.direction]
    
    def turn(self, turn_direction):
        """Turn left (-1) or right (1)"""
        self.direction = (self.direction + turn_direction) % 8
    
    def is_in_vision_cone(self, target_x, target_y, my_x, my_y):
        """Check if target is in vision cone"""
        dx = target_x - my_x
        dy = target_y - my_y
        
        if dx == 0 and dy == 0:
            return True
        
        # Calculate angle to target
        angle_to_target = math.degrees(math.atan2(dy, dx))
        
        # Calculate facing angle
        dir_dx, dir_dy = self.get_direction_vector()
        facing_angle = math.degrees(math.atan2(dir_dy, dir_dx))
        
        # Calculate angle difference
        angle_diff = abs(angle_to_target - facing_angle)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        return angle_diff <= self.vision_cone_angle / 2
