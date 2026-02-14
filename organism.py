import random
import numpy as np
from config import *

class Organism:
    """A digital life form that can move, eat, and reproduce"""
    
    def __init__(self, x, y, genome=None):
        self.x = x
        self.y = y
        self.energy = ORGANISM_START_ENERGY
        self.age = 0
        self.generation = 0
        
        # Genome - the "DNA" that defines behavior
        if genome is None:
            self.genome = self._create_random_genome()
        else:
            self.genome = genome.copy()
            self.generation = genome.get('generation', 0) + 1
    
    def _create_random_genome(self):
        """Create random genetic code"""
        return {
            'move_probability': random.random(),  # How often to move
            'move_randomness': random.random(),   # How random movement is
            'eat_threshold': random.random() * 50,  # Min energy in cell to eat
            'reproduce_threshold': MIN_ENERGY_TO_REPLICATE + random.random() * 100,
            'generation': 0,
            'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        }
    
    def mutate_genome(self):
        """Mutate genome during reproduction"""
        mutated = self.genome.copy()
        
        if random.random() < MUTATION_RATE:
            # Choose random gene to mutate
            gene = random.choice(['move_probability', 'move_randomness', 'eat_threshold', 'reproduce_threshold'])
            
            if gene in ['move_probability', 'move_randomness']:
                mutated[gene] = max(0, min(1, mutated[gene] + random.gauss(0, MUTATION_STRENGTH)))
            elif gene == 'eat_threshold':
                mutated[gene] = max(0, mutated[gene] + random.gauss(0, 10))
            elif gene == 'reproduce_threshold':
                mutated[gene] = max(MIN_ENERGY_TO_REPLICATE, mutated[gene] + random.gauss(0, 20))
            
            # Mutate color slightly
            if random.random() < 0.3:
                r, g, b = mutated['color']
                mutated['color'] = (
                    max(50, min(255, r + random.randint(-20, 20))),
                    max(50, min(255, g + random.randint(-20, 20))),
                    max(50, min(255, b + random.randint(-20, 20)))
                )
        
        return mutated
    
    def sense_environment(self, universe):
        """Look around and sense nearby energy"""
        nearby_energy = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                energy = universe.get_energy(self.x + dx, self.y + dy)
                nearby_energy.append((dx, dy, energy))
        return nearby_energy
    
    def decide_move(self, universe):
        """Decide where to move based on genome and environment"""
        if random.random() > self.genome['move_probability']:
            return 0, 0  # Don't move
        
        nearby = self.sense_environment(universe)
        
        # Mix of random and energy-seeking behavior
        if random.random() < self.genome['move_randomness']:
            # Random move
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
        else:
            # Move toward highest energy
            if nearby:
                best = max(nearby, key=lambda x: x[2])
                dx, dy = best[0], best[1]
            else:
                dx, dy = 0, 0
        
        return dx, dy
    
    def move(self, dx, dy, universe):
        """Move to new position"""
        new_x = (self.x + dx) % universe.width
        new_y = (self.y + dy) % universe.height
        
        self.x = new_x
        self.y = new_y
        self.energy -= ENERGY_COST_MOVE
    
    def eat(self, universe):
        """Try to eat energy from current cell"""
        available = universe.get_energy(self.x, self.y)
        
        if available >= self.genome['eat_threshold']:
            consumed = universe.consume_energy(self.x, self.y, available)
            self.energy += consumed
    
    def update(self, universe):
        """Update organism one time step"""
        self.age += 1
        
        # Cost of living
        self.energy -= ENERGY_COST_ALIVE
        
        # Decide and execute move
        dx, dy = self.decide_move(universe)
        if dx != 0 or dy != 0:
            self.move(dx, dy, universe)
        
        # Try to eat
        self.eat(universe)
        
        # Die of old age
        if self.age > MAX_ORGANISM_AGE:
            self.energy = 0
    
    def try_reproduce(self, universe):
        """Try to create offspring"""
        if self.energy >= self.genome['reproduce_threshold']:
            if len(universe.organisms) < MAX_POPULATION:
                # Pay reproduction cost
                self.energy -= ENERGY_COST_REPLICATE
                
                # Create offspring with mutated genome
                mutated_genome = self.mutate_genome()
                
                # Offspring spawns nearby
                offset_x = random.choice([-1, 0, 1])
                offset_y = random.choice([-1, 0, 1])
                child_x = (self.x + offset_x) % universe.width
                child_y = (self.y + offset_y) % universe.height
                
                offspring = Organism(child_x, child_y, mutated_genome)
                return offspring
        
        return None
    
    def is_dead(self):
        """Check if organism is dead"""
        return self.energy <= 0
    
    def get_color(self):
        """Get organism color for visualization"""
        return self.genome['color']
