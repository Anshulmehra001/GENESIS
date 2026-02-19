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
        
        # Phase 2: Communication signals
        if ENABLE_COMMUNICATION:
            self.signals = []
        
        # Phase 3: Structures
        if ENABLE_STRUCTURES:
            self.structures = []
        
        # Phase 3: Puzzles
        if ENABLE_PUZZLES:
            self.puzzles = []
        
        # Phase 3: Social hierarchies
        if ENABLE_HIERARCHY:
            from social_hierarchy import SocialHierarchy
            self.hierarchies = []
        
        # Statistics
        self.stats = {
            'total_births': 0,
            'total_deaths': 0,
            'total_energy_consumed': 0,
            'peak_population': 0,
            'predator_count': 0,
            'prey_count': 0,
            'signals_emitted': 0,
            'structures_built': 0,
            'puzzles_solved': 0
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
        
        # Update predator/prey counts
        if hasattr(organism, 'is_predator') and organism.is_predator:
            self.stats['predator_count'] = self.stats.get('predator_count', 0) + 1
        else:
            self.stats['prey_count'] = self.stats.get('prey_count', 0) + 1
    
    def remove_organism(self, organism):
        """Remove dead organism"""
        if organism in self.organisms:
            self.organisms.remove(organism)
            self.stats['total_deaths'] += 1
            
            # Update predator/prey counts
            if hasattr(organism, 'is_predator') and organism.is_predator:
                self.stats['predator_count'] = max(0, self.stats.get('predator_count', 0) - 1)
            else:
                self.stats['prey_count'] = max(0, self.stats.get('prey_count', 0) - 1)
    
    def add_signal(self, signal):
        """Add a communication signal"""
        if ENABLE_COMMUNICATION and len(self.signals) < MAX_SIGNALS:
            self.signals.append(signal)
            self.stats['signals_emitted'] = self.stats.get('signals_emitted', 0) + 1
    
    def add_structure(self, structure):
        """Add a structure to the universe"""
        if ENABLE_STRUCTURES and len(self.structures) < MAX_STRUCTURES:
            self.structures.append(structure)
            self.stats['structures_built'] = self.stats.get('structures_built', 0) + 1
    
    def add_puzzle(self, puzzle):
        """Add a puzzle to the universe"""
        if ENABLE_PUZZLES and len(self.puzzles) < MAX_PUZZLES:
            self.puzzles.append(puzzle)
    
    def update(self):
        """Update universe one time step"""
        self.tick += 1
        
        # Spawn new energy
        self.spawn_energy()
        
        # Phase 2: Update signals
        if ENABLE_COMMUNICATION:
            expired_signals = []
            for signal in self.signals:
                signal.update()
                if signal.is_expired():
                    expired_signals.append(signal)
            
            for signal in expired_signals:
                self.signals.remove(signal)
        
        # Phase 3: Update structures
        if ENABLE_STRUCTURES:
            destroyed_structures = []
            for structure in self.structures:
                structure.update()
                if structure.is_destroyed():
                    destroyed_structures.append(structure)
            
            for structure in destroyed_structures:
                self.structures.remove(structure)
        
        # Phase 3: Spawn puzzles occasionally
        if ENABLE_PUZZLES and random.random() < PUZZLE_SPAWN_CHANCE:
            if len(self.puzzles) < MAX_PUZZLES:
                from problem_solving import Puzzle
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                puzzle_type = random.choice(['maze', 'locked_resource', 'multi_step'])
                puzzle = Puzzle(x, y, puzzle_type)
                self.add_puzzle(puzzle)
        
        # Phase 2: Occasionally spawn predators
        if ENABLE_PREDATORS and random.random() < PREDATOR_SPAWN_CHANCE:
            if self.stats.get('predator_count', 0) < len(self.organisms) * 0.1:  # Max 10% predators
                from predator import Predator
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                predator = Predator(x, y)
                self.add_organism(predator)
        
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
        stats = {
            'tick': self.tick,
            'population': len(self.organisms),
            'total_births': self.stats['total_births'],
            'total_deaths': self.stats['total_deaths'],
            'total_energy': np.sum(self.energy_grid),
            'avg_organism_energy': np.mean([o.energy for o in self.organisms]) if self.organisms else 0,
            'peak_population': self.stats['peak_population']
        }
        
        # Phase 2 stats
        if ENABLE_PREDATORS:
            stats['predator_count'] = self.stats.get('predator_count', 0)
            stats['prey_count'] = self.stats.get('prey_count', 0)
        
        if ENABLE_COMMUNICATION:
            stats['active_signals'] = len(self.signals) if hasattr(self, 'signals') else 0
            stats['signals_emitted'] = self.stats.get('signals_emitted', 0)
        
        return stats
