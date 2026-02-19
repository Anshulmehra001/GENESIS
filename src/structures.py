"""
Environmental Structures and Tools
Organisms can create and use structures
"""

class Structure:
    """A structure placed in the environment"""
    
    def __init__(self, x, y, structure_type, creator):
        self.x = x
        self.y = y
        self.type = structure_type  # 'wall', 'trap', 'storage', 'shelter'
        self.creator = creator
        self.durability = 100
        self.stored_energy = 0
        self.age = 0
    
    def update(self):
        """Age and decay structure"""
        self.age += 1
        self.durability -= 0.1
    
    def is_destroyed(self):
        """Check if structure is destroyed"""
        return self.durability <= 0
    
    def get_benefit(self, organism):
        """Get benefit from structure"""
        if self.type == 'shelter':
            return {'protection': 0.5}  # 50% damage reduction
        elif self.type == 'storage' and self.stored_energy > 0:
            return {'energy': min(50, self.stored_energy)}
        elif self.type == 'trap':
            return {'trapped': True}
        return {}
    
    def store_energy(self, amount):
        """Store energy in structure"""
        if self.type == 'storage':
            self.stored_energy += amount
            return True
        return False


class Tool:
    """A tool that enhances organism capabilities"""
    
    def __init__(self, tool_type):
        self.type = tool_type  # 'digger', 'weapon', 'sensor'
        self.durability = 50
        self.efficiency = 1.5
    
    def use(self):
        """Use tool, reducing durability"""
        self.durability -= 1
        return self.efficiency if self.durability > 0 else 1.0
    
    def is_broken(self):
        """Check if tool is broken"""
        return self.durability <= 0
