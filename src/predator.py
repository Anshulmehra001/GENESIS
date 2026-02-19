"""
Predator Organism
Can hunt and consume other organisms for energy
"""

import random
import numpy as np
from organism import Organism
from config import *

class Predator(Organism):
    """Predator organism that hunts prey"""
    
    def __init__(self, x, y, genome=None):
        super().__init__(x, y, genome)
        self.is_predator = True
        
        # Predators have different color scheme (red tones)
        if genome is None:
            r, g, b = self.genome['color']
            self.genome['color'] = (min(255, r + 100), max(0, g - 50), max(0, b - 50))
    
    def sense_prey(self, universe):
        """Detect nearby prey organisms"""
        nearby_prey = []
        vision_range = 5
        
        for organism in universe.organisms:
            if organism is self or getattr(organism, 'is_predator', False):
                continue
            
            dx = organism.x - self.x
            dy = organism.y - self.y
            
            # Handle wrap-around (find shortest path)
            if abs(dx) > universe.width / 2:
                dx = dx - universe.width if dx > 0 else dx + universe.width
            if abs(dy) > universe.height / 2:
                dy = dy - universe.height if dy > 0 else dy + universe.height
            
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= vision_range:
                # Phase 2: Directional sensing - only see in forward cone
                if ENABLE_DIRECTIONAL_SENSING:
                    if not self._is_in_vision_cone(int(dx), int(dy)):
                        continue
                
                nearby_prey.append((organism, dx, dy, distance))
        
        return nearby_prey
    
    def decide_move(self, universe):
        """Decide where to move - hunt prey or seek energy"""
        if random.random() > self.genome['move_probability']:
            return 0, 0
        
        # First priority: hunt nearby prey
        nearby_prey = self.sense_prey(universe)
        
        if nearby_prey and random.random() < 0.7:  # 70% chance to hunt
            # Move toward closest prey
            target, dx, dy, distance = min(nearby_prey, key=lambda x: x[3])
            
            move_x = 1 if target.x > self.x else -1 if target.x < self.x else 0
            move_y = 1 if target.y > self.y else -1 if target.y < self.y else 0
            
            return move_x, move_y
        
        # Fallback: normal energy-seeking behavior
        return super().decide_move(universe)
    
    def try_hunt(self, universe):
        """Try to catch and eat prey at current location"""
        for organism in universe.organisms:
            if organism is self or getattr(organism, 'is_predator', False):
                continue
            
            # Check if prey is at same location
            if organism.x == self.x and organism.y == self.y:
                # Successful hunt!
                energy_gained = organism.energy * 0.5  # Get 50% of prey's energy
                self.energy += energy_gained
                organism.energy = 0  # Kill the prey
                
                # Emit alarm signal
                if hasattr(universe, 'signals'):
                    from signal import Signal
                    universe.add_signal(Signal(self.x, self.y, 'alarm', 2.0))
                
                return True
        
        return False
    
    def update(self, universe):
        """Update predator - hunt then normal update"""
        self.age += 1
        self.energy -= ENERGY_COST_ALIVE * 1.5  # Predators cost more energy
        
        # Try to hunt
        self.try_hunt(universe)
        
        # Decide and execute move
        dx, dy = self.decide_move(universe)
        if dx != 0 or dy != 0:
            self.move(dx, dy, universe)
        
        # Try to eat energy (predators can also eat plants)
        self.eat(universe)
        
        # Die of old age
        if self.age > MAX_ORGANISM_AGE:
            self.energy = 0
