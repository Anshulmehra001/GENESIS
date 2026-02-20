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
        
        # Phase 2: Directional sensing
        if ENABLE_DIRECTIONAL_SENSING:
            self.direction = random.randint(0, 7)  # 0=N, 1=NE, 2=E, 3=SE, 4=S, 5=SW, 6=W, 7=NW
        
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
        
        # Phase 4: Abstract Reasoning
        if ENABLE_ABSTRACT_REASONING:
            from abstract_reasoning import AbstractReasoning
            self.reasoning = AbstractReasoning(self)
        
        # Phase 4: Language
        if ENABLE_LANGUAGE:
            from language_system import LanguageSystem
            self.language = LanguageSystem(self)
        
        # Phase 4: Self-Awareness
        if ENABLE_SELF_AWARENESS:
            from self_awareness import SelfAwareness
            self.self_awareness = SelfAwareness(self)
        
        # Phase 4: Creativity
        if ENABLE_CREATIVITY:
            from creativity import CreativitySystem
            self.creativity = CreativitySystem(self)
        
        # Phase 4.5: Self-Modification (Experimental)
        if ENABLE_SELF_MODIFICATION:
            from self_modification import SelfModificationSystem
            self.self_modification = SelfModificationSystem(self)
        
        # Phase 5: AGI Emergence
        if ENABLE_GENERAL_INTELLIGENCE:
            from agi_emergence import GeneralIntelligence
            self.agi = GeneralIntelligence(self)
        
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
        
        # Phase 4: Cognitive genes
        if ENABLE_ABSTRACT_REASONING:
            genome['pattern_recognition'] = random.random()
            genome['causal_reasoning'] = random.random()
        
        if ENABLE_LANGUAGE:
            genome['language_ability'] = random.random()
            genome['innovation_tendency'] = random.random()
        
        if ENABLE_CREATIVITY:
            genome['curiosity'] = random.random()
            genome['exploration_tendency'] = random.random()
        
        if ENABLE_SELF_AWARENESS:
            genome['self_reflection'] = random.random()
            genome['theory_of_mind'] = random.random()
        
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
            if ENABLE_ABSTRACT_REASONING:
                genes.extend(['pattern_recognition', 'causal_reasoning'])
            if ENABLE_LANGUAGE:
                genes.extend(['language_ability', 'innovation_tendency'])
            if ENABLE_CREATIVITY:
                genes.extend(['curiosity', 'exploration_tendency'])
            if ENABLE_SELF_AWARENESS:
                genes.extend(['self_reflection', 'theory_of_mind'])
            
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
                
                # Phase 2: Directional sensing - only see in forward cone
                if ENABLE_DIRECTIONAL_SENSING:
                    if not self._is_in_vision_cone(dx, dy):
                        continue
                
                energy = universe.get_energy(self.x + dx, self.y + dy)
                nearby_energy.append((dx, dy, energy))
        
        return nearby_energy
    
    def _is_in_vision_cone(self, dx, dy):
        """Check if a relative position is within the forward vision cone"""
        if dx == 0 and dy == 0:
            return True
        
        # Calculate angle to target relative to facing direction
        import math
        
        # Direction vectors for each of 8 directions
        direction_vectors = [
            (0, -1),   # 0: North
            (1, -1),   # 1: NE
            (1, 0),    # 2: East
            (1, 1),    # 3: SE
            (0, 1),    # 4: South
            (-1, 1),   # 5: SW
            (-1, 0),   # 6: West
            (-1, -1)   # 7: NW
        ]
        
        facing_dx, facing_dy = direction_vectors[self.direction]
        
        # Calculate angle between facing direction and target
        # Using dot product to determine if target is in front
        dot_product = dx * facing_dx + dy * facing_dy
        
        # Normalize vectors
        facing_mag = math.sqrt(facing_dx**2 + facing_dy**2)
        target_mag = math.sqrt(dx**2 + dy**2)
        
        if facing_mag == 0 or target_mag == 0:
            return True
        
        # Calculate angle
        cos_angle = dot_product / (facing_mag * target_mag)
        angle_rad = math.acos(max(-1, min(1, cos_angle)))
        angle_deg = math.degrees(angle_rad)
        
        # Check if within vision cone
        return angle_deg <= (VISION_CONE_ANGLE / 2)
    
    def sense_organisms(self, universe):
        """Detect nearby organisms"""
        if not ENABLE_SOCIAL:
            return []
        
        nearby = []
        for organism in universe.organisms:
            if organism is self:
                continue
            
            dx = organism.x - self.x
            dy = organism.y - self.y
            
            # Handle wrap-around (find shortest path)
            if abs(dx) > universe.width / 2:
                dx = dx - universe.width if dx > 0 else dx + universe.width
            if abs(dy) > universe.height / 2:
                dy = dy - universe.height if dy > 0 else dy + universe.height
            
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= VISION_RANGE:
                # Phase 2: Directional sensing - only see in forward cone
                if ENABLE_DIRECTIONAL_SENSING:
                    if not self._is_in_vision_cone(int(dx), int(dy)):
                        continue
                
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
        
        # Phase 2: Include directional information
        direction_input = self.direction / 7.0 if ENABLE_DIRECTIONAL_SENSING else 0.5
        
        inputs = [
            energy_n / 100, energy_s / 100, energy_e / 100, energy_w / 100,
            energy_here / 100,
            self.energy / 500,
            self.age / 1000,
            len(self.sense_organisms(universe)) / 10,
            direction_input,  # Current facing direction
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
        
        # Phase 2: Directional sensing - update direction and pay turning cost
        if ENABLE_DIRECTIONAL_SENSING and (dx != 0 or dy != 0):
            # Map movement to direction (0-7)
            direction_map = {
                (0, -1): 0,   # North
                (1, -1): 1,   # NE
                (1, 0): 2,    # East
                (1, 1): 3,    # SE
                (0, 1): 4,    # South
                (-1, 1): 5,   # SW
                (-1, 0): 6,   # West
                (-1, -1): 7   # NW
            }
            
            new_direction = direction_map.get((dx, dy), self.direction)
            
            # Pay energy cost for turning
            if new_direction != self.direction:
                self.energy -= ENERGY_COST_TURN
                self.direction = new_direction
        
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
        
        # Phase 4: Abstract Reasoning - observe and learn patterns
        if ENABLE_ABSTRACT_REASONING:
            observation = {
                'energy_here': universe.get_energy(self.x, self.y),
                'age': self.age,
                'energy': self.energy
            }
            self.reasoning.observe(observation)
        
        # Phase 4: Language - occasionally communicate
        if ENABLE_LANGUAGE and random.random() < self.genome.get('language_ability', 0.1):
            if self.energy < 100:
                utterance = self.language.express('need_energy')
                if utterance:
                    # Broadcast to nearby organisms
                    nearby = self.sense_organisms(universe)
                    for other, _ in nearby[:3]:
                        if hasattr(other, 'language'):
                            other.language.comprehend(utterance)
        
        # Phase 4: Self-Awareness - reflect periodically
        if ENABLE_SELF_AWARENESS:
            action = self.self_awareness.reflect(universe.tick)
            if action == 'change_strategy':
                # Change behavior based on reflection
                self.genome['move_randomness'] = random.random()
        
        # Phase 4: Creativity - explore or exploit
        if ENABLE_CREATIVITY:
            state = (self.x, self.y, self.energy)
            self.creativity.record_state_visit(state)
            
            # Occasionally try novel behavior
            if self.creativity.should_explore(state):
                novel = self.creativity.generate_novel_behavior(state)
                # Try novel behavior (simplified)
                if novel and random.random() < 0.5:
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])
                    self.move(dx, dy, universe)
                    return  # Skip normal behavior
        
        # Phase 4.5: Self-Modification - occasionally try to improve self
        if ENABLE_SELF_MODIFICATION and hasattr(self, 'self_modification'):
            if random.random() < 0.001:  # Rare
                modification = self.self_modification.propose_modification()
                if modification:
                    if self.self_modification.test_modification(modification):
                        self.self_modification.apply_modification(modification)
        
        # Phase 5: AGI - pursue autonomous goals
        if ENABLE_GENERAL_INTELLIGENCE and hasattr(self, 'agi'):
            # Measure consciousness
            if CALCULATE_PHI and random.random() < 0.01:
                self.agi.measure_consciousness()
            
            # Pursue current goal
            if ENABLE_AUTONOMOUS_GOALS:
                goal = self.agi.pursue_goal()
                
                # Goal might influence behavior
                if goal and goal.description == 'explore_environment':
                    # Exploration behavior
                    if random.random() < 0.3:
                        dx = random.choice([-1, 0, 1])
                        dy = random.choice([-1, 0, 1])
                        self.move(dx, dy, universe)
                        return
            
            # Novelty search
            if ENABLE_NOVELTY_SEARCH:
                current_behavior = (self.x, self.y, self.age)
                novelty = self.agi.calculate_novelty(current_behavior)
                
                if novelty > 0.7:
                    # Novel behavior! Archive it
                    self.agi.archive_behavior(current_behavior)
                    # Reward novelty
                    self.energy += NOVELTY_REWARD_MULTIPLIER
        
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
