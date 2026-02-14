import numpy as np
import random
from config import *

class Universe:
    """The digital world where artificial life exists"""
    
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.tick = 0
        
        # Energy grid - where resources exist
        self.energy_grid = np.zeros((self.height, self.width))
        
        # Initialize with some energy
        self._spawn_initial_energy()
        
        # Organisms list
        self.organisms = []
        
        # Statistics
        self.stats = {
            'total_births': 0,
            'total_deaths': 0,
            'total_energy_consumed': 0,
            'peak_population': 0
        }
    
    def _spawn_initial_energy(self):
        """Distribute initial energy across the grid"""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < INITIAL_ENERGY_DISTRIBUTION:
                    self.energy_grid[y][x] = ENERGY_AMOUNT
    
    def spawn_energy(self):
        """Randomly spawn energy in the universe"""
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < ENERGY_SPAWN_RATE:
                    self.energy_grid[y][x] = min(
                        self.energy_grid[y][x] + ENERGY_AMOUNT,
                        MAX_ENERGY_PER_CELL
                    )
    
    def get_energy(self, x, y):
        """Get energy at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.energy_grid[y][x]
        return 0
    
    def consume_energy(self, x, y, amount):
        """Organism consumes energy from a cell"""
        if 0 <= x < self.width and 0 <= y < self.height:
            available = self.energy_grid[y][x]
            consumed = min(available, amount)
            self.energy_grid[y][x] -= consumed
            self.stats['total_energy_consumed'] += consumed
            return consumed
        return 0
    
    def add_organism(self, organism):
        """Add organism to universe"""
        self.organisms.append(organism)
        self.stats['total_births'] += 1
        self.stats['peak_population'] = max(
            self.stats['peak_population'],
            len(self.organisms)
        )
    
    def remove_organism(self, organism):
        """Remove dead organism"""
        if organism in self.organisms:
            self.organisms.remove(organism)
            self.stats['total_deaths'] += 1
    
    def update(self):
        """Update universe one time step"""
        self.tick += 1
        
        # Spawn new energy
        self.spawn_energy()
        
        # Update all organisms
        dead_organisms = []
        new_organisms = []
        
        for organism in self.organisms:
            organism.update(self)
            
            # Check if organism died
            if organism.is_dead():
                dead_organisms.append(organism)
            
            # Check if organism reproduced
            offspring = organism.try_reproduce(self)
            if offspring:
                new_organisms.append(offspring)
        
        # Remove dead organisms
        for organism in dead_organisms:
            self.remove_organism(organism)
        
        # Add new organisms
        for organism in new_organisms:
            self.add_organism(organism)
        
        # Safety check
        if len(self.organisms) > EMERGENCY_STOP_POPULATION:
            print(f"⚠️ EMERGENCY STOP: Population exceeded {EMERGENCY_STOP_POPULATION}")
            return False
        
        return True
    
    def get_stats(self):
        """Get current statistics"""
        return {
            'tick': self.tick,
            'population': len(self.organisms),
            'total_births': self.stats['total_births'],
            'total_deaths': self.stats['total_deaths'],
            'total_energy': np.sum(self.energy_grid),
            'avg_organism_energy': np.mean([o.energy for o in self.organisms]) if self.organisms else 0,
            'peak_population': self.stats['peak_population']
        }
