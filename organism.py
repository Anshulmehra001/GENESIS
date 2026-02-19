import random
import numpy as np
from config import *

if USE_NEURAL_NETWORKS:
    from neural_network import NeuralNetwork

class Organism:
    """A digital life form that can move, eat, and reproduce"""
    
    def __init__(self, x, y, genome=None, parent=None):
        self.x = x
        self.y = y
        self.energy = ORGANISM_START_ENERGY
        self.age = 0
        self.generation = 0
        self.is_predator = False
        self.parent = parent
        
        # Phase 2: Memory system
        if ENABLE_MEMORY:
            self.memory = []  # List of (x, y, energy_found) tuples
            self.visited_recently = set()
        
        # Phase 3: Multi-cellular
        if ENABLE_MULTICELLULAR:
            self.cells = [self]  # List of cells in this organism
            self.is_multicellular = False
        
        # Phase 3: Social
        if ENABLE_SOCIAL:
            self.kin = []  # List of recognized kin
            self.group = None
        
        # Genome - the "DNA" that defines behavior
        if genome is None:
            self.genome = self._create_random_genome()
        else:
            self.genome = genome.copy()
            self.generation = genome.get('generation', 0) + 1
            
            # Copy neural network if using them
            if USE_NEURAL_NETWORKS and 'brain' in genome:
                self.genome['brain'] = genome['brain'].copy()
    
    def _create_random_genome(self):
        """Create random genetic code"""
        genome = {
            'move_probability': random.random(),
            'move_randomness': random.random(),
            'eat_threshold': random.random() * 50,
            'reproduce_threshold': MIN_ENERGY_TO_REPLICATE + random.random() * 100,
            'generation': 0,
            'color': (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        }
        
        # Phase 2: Add neural network brain
        if USE_NEURAL_NETWORKS:
            genome['brain'] = NeuralNetwork(
                input_size=10,
                hidden_sizes=NEURAL_HIDDEN_LAYERS,
                output_size=6
            )
        
        # Phase 2: Communication genes
        if ENABLE_COMMUNICATION:
            genome['signal_probability'] = random.random() * 0.1
            genome['signal_response'] = random.random()
        
        # Phase 3: Social genes
        if ENABLE_SOCIAL:
            genome['cooperation'] = random.random()
            genome['aggression'] = random.random()
        
        return genome
    
    def mutate_genome(self):
        """Mutate genome during reproduction"""
        mutated = self.genome.copy()
        
        # Mutate neural network if using them
        if USE_NEURAL_NETWORKS and 'brain' in mutated:
            mutated['brain'] = mutated['brain'].copy()
            mutated['brain'].mutate(NEURAL_MUTATION_RATE, NEURAL_MUTATION_STRENGTH)
        
        if random.random() < MUTATION_RATE:
            # Choose random gene to mutate
            genes = ['move_probability', 'move_randomness', 'eat_threshold', 'reproduce_threshold']
            
            if ENABLE_COMMUNICATION:
                genes.extend(['signal_probability', 'signal_response'])
            if ENABLE_SOCIAL:
                genes.extend(['cooperation', 'aggression'])
            
            gene = random.choice(genes)
            
            if gene in ['move_probability', 'move_randomness', 'signal_probability', 
                       'signal_response', 'cooperation', 'aggression']:
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
        vision = VISION_RANGE if ENABLE_MEMORY else 1
        
        for dx in range(-vision, vision + 1):
            for dy in range(-vision, vision + 1):
                if dx == 0 and dy == 0:
                    continue
                energy = universe.get_energy(self.x + dx, self.y + dy)
                nearby_energy.append((dx, dy, energy))
        
        return nearby_energy
    
    def sense_organisms(self, universe):
        """Detect nearby organisms"""
        if not ENABLE_SOCIAL:
            return []
        
        nearby = []
        for organism in universe.organisms:
            if organism is self:
                continue
            
            dx = abs(organism.x - self.x)
            dy = abs(organism.y - self.y)
            
            # Handle wrap-around
            dx = min(dx, universe.width - dx)
            dy = min(dy, universe.height - dy)
            
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= VISION_RANGE:
                nearby.append((organism, distance))
        
        return nearby
    
    def sense_signals(self, universe):
        """Detect nearby communication signals"""
        if not ENABLE_COMMUNICATION or not hasattr(universe, 'signals'):
            return []
        
        nearby_signals = []
        for signal in universe.signals:
            strength = signal.get_strength_at(self.x, self.y)
            if strength > 0.1:
                nearby_signals.append((signal, strength))
        
        return nearby_signals
    
    def emit_signal(self, universe, signal_type):
        """Emit a communication signal"""
        if not ENABLE_COMMUNICATION or self.energy < SIGNAL_COST:
            return
        
        if hasattr(universe, 'add_signal'):
            from signal import Signal
            universe.add_signal(Signal(self.x, self.y, signal_type, 1.0))
            self.energy -= SIGNAL_COST
    
    def decide_move(self, universe):
        """Decide where to move based on genome and environment"""
        if random.random() > self.genome['move_probability']:
            return 0, 0  # Don't move
        
        # Phase 2: Use neural network for decision making
        if USE_NEURAL_NETWORKS and 'brain' in self.genome:
            return self._neural_decide_move(universe)
        
        # Phase 2: Check signals
        if ENABLE_COMMUNICATION:
            signals = self.sense_signals(universe)
            for signal, strength in signals:
                if signal.type == 'alarm' and strength > 0.5:
                    # Flee from alarm
                    dx = 1 if self.x < signal.x else -1 if self.x > signal.x else 0
                    dy = 1 if self.y < signal.y else -1 if self.y > signal.y else 0
                    return -dx, -dy  # Move away
                elif signal.type == 'food' and strength > 0.5:
                    # Move toward food signal
                    dx = 1 if signal.x > self.x else -1 if signal.x < self.x else 0
                    dy = 1 if signal.y > self.y else -1 if signal.y < self.y else 0
                    return dx, dy
        
        # Phase 2: Check memory for good locations
        if ENABLE_MEMORY and self.memory:
            # Sometimes revisit high-energy locations
            if random.random() < 0.3:
                best_memory = max(self.memory, key=lambda m: m[2])
                mx, my, _ = best_memory
                dx = 1 if mx > self.x else -1 if mx < self.x else 0
                dy = 1 if my > self.y else -1 if my < self.y else 0
                return dx, dy
        
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
    
    def _neural_decide_move(self, universe):
        """Use neural network to decide movement"""
        # Prepare inputs
        nearby = self.sense_environment(universe)
        
        # Get energy in 4 directions
        energy_n = sum(e for dx, dy, e in nearby if dy < 0) / max(1, sum(1 for dx, dy, e in nearby if dy < 0))
        energy_s = sum(e for dx, dy, e in nearby if dy > 0) / max(1, sum(1 for dx, dy, e in nearby if dy > 0))
        energy_e = sum(e for dx, dy, e in nearby if dx > 0) / max(1, sum(1 for dx, dy, e in nearby if dx > 0))
        energy_w = sum(e for dx, dy, e in nearby if dx < 0) / max(1, sum(1 for dx, dy, e in nearby if dx < 0))
        
        energy_here = universe.get_energy(self.x, self.y)
        
        inputs = [
            energy_n / 100, energy_s / 100, energy_e / 100, energy_w / 100,
            energy_here / 100,
            self.energy / 500,
            self.age / 1000,
            len(self.sense_organisms(universe)) / 10,
            random.random(),  # Noise
            random.random()   # Noise
        ]
        
        # Get network output
        outputs = self.genome['brain'].forward(inputs)
        
        # Interpret outputs: [move_n, move_s, move_e, move_w, eat, reproduce]
        move_n, move_s, move_e, move_w, eat_signal, reproduce_signal = outputs
        
        # Choose direction with highest activation
        dx = 0
        dy = 0
        
        if move_e > 0.5 and move_e > move_w:
            dx = 1
        elif move_w > 0.5:
            dx = -1
        
        if move_s > 0.5 and move_s > move_n:
            dy = 1
        elif move_n > 0.5:
            dy = -1
        
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
        
        # Phase 2: Update memory
        if ENABLE_MEMORY:
            energy_here = universe.get_energy(self.x, self.y)
            if energy_here > 50:
                # Remember this location
                self.memory.append((self.x, self.y, energy_here))
                if len(self.memory) > MEMORY_SIZE:
                    self.memory.pop(0)
        
        # Phase 2: Emit signals occasionally
        if ENABLE_COMMUNICATION and random.random() < self.genome.get('signal_probability', 0):
            if self.energy < 100:
                self.emit_signal(universe, 'alarm')
            elif universe.get_energy(self.x, self.y) > 100:
                self.emit_signal(universe, 'food')
        
        # Phase 3: Recognize kin
        if ENABLE_SOCIAL and random.random() < 0.1:
            nearby_organisms = self.sense_organisms(universe)
            for organism, distance in nearby_organisms:
                if self._is_kin(organism):
                    if organism not in self.kin:
                        self.kin.append(organism)
        
        # Decide and execute move
        dx, dy = self.decide_move(universe)
        if dx != 0 or dy != 0:
            self.move(dx, dy, universe)
        
        # Try to eat
        self.eat(universe)
        
        # Die of old age
        if self.age > MAX_ORGANISM_AGE:
            self.energy = 0
    
    def _is_kin(self, other):
        """Check if another organism is kin (similar genome)"""
        if not ENABLE_SOCIAL:
            return False
        
        # Simple kin recognition based on color similarity
        r1, g1, b1 = self.genome['color']
        r2, g2, b2 = other.genome['color']
        
        color_distance = ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) ** 0.5
        max_distance = (255**2 * 3) ** 0.5
        
        similarity = 1 - (color_distance / max_distance)
        
        return similarity > KIN_RECOGNITION_THRESHOLD
    
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
                
                offspring = Organism(child_x, child_y, mutated_genome, parent=self)
                
                # Phase 3: Multi-cellular - chance to stay attached
                if ENABLE_MULTICELLULAR and random.random() < CELL_ADHESION_CHANCE:
                    if len(self.cells) < MAX_ORGANISM_SIZE:
                        self.cells.append(offspring)
                        offspring.cells = self.cells
                        self.is_multicellular = True
                        offspring.is_multicellular = True
                
                return offspring
        
        return None
    
    def is_dead(self):
        """Check if organism is dead"""
        return self.energy <= 0
    
    def get_color(self):
        """Get organism color for visualization"""
        return self.genome['color']
