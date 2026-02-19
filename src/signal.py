"""
Communication Signal System
Organisms can emit and detect signals for communication
"""

class Signal:
    """A communication signal emitted by an organism"""
    
    def __init__(self, x, y, signal_type, strength=1.0):
        self.x = x
        self.y = y
        self.type = signal_type  # 'alarm', 'food', 'mating'
        self.strength = strength
        self.age = 0
    
    def update(self):
        """Age the signal and decay its strength"""
        self.age += 1
        self.strength *= 0.9  # Decay by 10% per tick
    
    def is_expired(self):
        """Check if signal has decayed too much"""
        return self.strength < 0.1 or self.age > 50
    
    def get_strength_at(self, x, y):
        """Get signal strength at a given position"""
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        if distance > 10:  # Max range
            return 0
        return self.strength * (1 - distance / 10)
