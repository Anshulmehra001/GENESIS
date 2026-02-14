# GENESIS - Digital Biosphere Design Document

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GENESIS System                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │  Visualizer  │◄─────┤   Universe   │                   │
│  │   (Pygame)   │      │   (Physics)  │                   │
│  └──────────────┘      └───────┬──────┘                   │
│                                 │                           │
│                                 │ manages                   │
│                                 ▼                           │
│                        ┌─────────────────┐                 │
│                        │   Organisms     │                 │
│                        │  (Life Forms)   │                 │
│                        └────────┬────────┘                 │
│                                 │                           │
│                                 │ contains                  │
│                                 ▼                           │
│                        ┌─────────────────┐                 │
│                        │     Genome      │                 │
│                        │  (Genetic Code) │                 │
│                        └─────────────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Universe (universe.py)

**Purpose:** The digital world where all life exists. Manages physics, energy, and organism lifecycle.

**Key Responsibilities:**
- Maintain 2D grid world state
- Manage energy distribution and spawning
- Track all living organisms
- Execute simulation time steps
- Enforce safety limits
- Collect statistics

**Data Structures:**
```python
class Universe:
    - energy_grid: np.array[height, width]  # Energy at each location
    - organisms: List[Organism]              # All living organisms
    - tick: int                              # Current time step
    - stats: Dict                            # Global statistics
```

**Key Methods:**
- `update()`: Advance simulation one time step
- `spawn_energy()`: Add energy to random locations
- `consume_energy(x, y, amount)`: Remove energy from location
- `add_organism()`: Birth new organism
- `remove_organism()`: Handle organism death

**Physics Rules:**
- Toroidal topology (wrap-around edges)
- Discrete time (tick-based)
- Energy conservation (energy doesn't disappear, only transfers)
- Spatial locality (organisms only interact with nearby cells)

---

### 2. Organism (organism.py)

**Purpose:** Individual life form that can sense, move, eat, and reproduce.

**Key Responsibilities:**
- Maintain internal state (position, energy, age)
- Store genetic code (genome)
- Sense environment
- Make decisions based on genome
- Execute actions (move, eat, reproduce)
- Handle death conditions

**Data Structures:**
```python
class Organism:
    - x, y: int                    # Position in universe
    - energy: float                # Current energy level
    - age: int                     # Ticks since birth
    - generation: int              # Evolutionary generation
    - genome: Dict                 # Genetic code
```

**Genome Structure (Phase 1):**
```python
genome = {
    'move_probability': float,      # How often to move (0-1)
    'move_randomness': float,       # Random vs directed movement (0-1)
    'eat_threshold': float,         # Min energy in cell to eat
    'reproduce_threshold': float,   # Energy needed to reproduce
    'generation': int,              # Generation counter
    'color': (r, g, b)             # Visual identifier
}
```

**Decision-Making Algorithm:**
```
1. Sense environment (check nearby cells for energy)
2. Consult genome for behavioral parameters
3. Decide action:
   - Move: Based on move_probability and move_randomness
   - Eat: If current cell has energy >= eat_threshold
   - Reproduce: If energy >= reproduce_threshold
4. Execute action
5. Pay energy costs
6. Check death conditions
```

**Energy Economics:**
- Start energy: 200 units
- Cost to exist: 0.5 per tick
- Cost to move: 1 per move
- Cost to reproduce: 150 units
- Gain from eating: Variable (depends on cell energy)

---

### 3. Genetic System

**Purpose:** Enable evolution through heredity and variation.

**Inheritance:**
- Offspring receive copy of parent genome
- Generation counter increments
- Color inherits with slight variation

**Mutation:**
- Occurs during reproduction
- Probability: 10% (configurable)
- Affects random gene
- Mutation strength: ±20% of current value
- Bounded to valid ranges

**Mutation Algorithm:**
```python
def mutate_genome(parent_genome):
    child_genome = copy(parent_genome)
    
    if random() < MUTATION_RATE:
        gene = random_choice(['move_probability', 'move_randomness', 
                              'eat_threshold', 'reproduce_threshold'])
        
        if gene in ['move_probability', 'move_randomness']:
            # Bounded to [0, 1]
            child_genome[gene] += gaussian(0, MUTATION_STRENGTH)
            child_genome[gene] = clamp(child_genome[gene], 0, 1)
        
        elif gene == 'eat_threshold':
            # Bounded to [0, infinity]
            child_genome[gene] += gaussian(0, 10)
            child_genome[gene] = max(0, child_genome[gene])
        
        elif gene == 'reproduce_threshold':
            # Bounded to [MIN_ENERGY_TO_REPLICATE, infinity]
            child_genome[gene] += gaussian(0, 20)
            child_genome[gene] = max(MIN_ENERGY_TO_REPLICATE, 
                                     child_genome[gene])
    
    return child_genome
```

**Selection Pressure:**
- Organisms with better genes find food faster
- Better genes = more energy = more reproduction
- Poor genes = starvation = death
- No explicit fitness function (emergent selection)

---

### 4. Visualizer (visualizer.py)

**Purpose:** Real-time rendering of simulation state for observation.

**Rendering Layers:**
1. **Energy Layer** (background)
   - Green gradient based on energy amount
   - Brighter = more energy
   - Black = no energy

2. **Organism Layer** (foreground)
   - Colored circles
   - Color = genetic lineage
   - Size = energy level
   - Position = location in universe

3. **Statistics Layer** (UI overlay)
   - Current tick
   - Population count
   - Birth/death totals
   - Average energy
   - Total world energy

**User Controls:**
- SPACE: Pause/resume
- R: Reset simulation
- ESC: Quit

**Performance:**
- Target: 30 FPS
- Adaptive rendering (skip frames if needed)
- Efficient drawing (only changed cells)

---

## Data Flow

### Simulation Loop

```
1. User Input
   ↓
2. Universe.update()
   ├─ Spawn energy in random cells
   ├─ For each organism:
   │  ├─ organism.update(universe)
   │  │  ├─ Age increment
   │  │  ├─ Pay existence cost
   │  │  ├─ Sense environment
   │  │  ├─ Decide move
   │  │  ├─ Execute move (pay cost)
   │  │  ├─ Try to eat
   │  │  └─ Check death conditions
   │  ├─ organism.try_reproduce()
   │  │  ├─ Check energy threshold
   │  │  ├─ Pay reproduction cost
   │  │  ├─ Mutate genome
   │  │  └─ Create offspring
   │  └─ Collect dead organisms
   ├─ Remove dead organisms
   ├─ Add new organisms
   └─ Update statistics
   ↓
3. Visualizer.render()
   ├─ Draw energy grid
   ├─ Draw organisms
   └─ Draw statistics
   ↓
4. Repeat
```

---

## Evolution Dynamics

### Expected Evolutionary Trajectory

**Generation 0-10 (Ticks 0-100):**
- High mortality (most die quickly)
- Random exploration
- Population crash

**Generation 10-100 (Ticks 100-1000):**
- Survivors have better genes
- Energy-seeking behavior emerges
- Population stabilizes
- Genetic diversity increases

**Generation 100-1000 (Ticks 1000-10000):**
- Optimized movement strategies
- Efficient energy consumption
- Stable population cycles
- Distinct lineages (color groups)

**Generation 1000+ (Ticks 10000+):**
- Highly adapted organisms
- Ecological balance
- Potential for new behaviors
- Foundation for Phase 2 complexity

### Fitness Landscape

No explicit fitness function. Fitness emerges from:
- Energy acquisition efficiency
- Energy conservation
- Reproduction timing
- Movement strategy
- Environmental awareness

**Optimal Strategy (Predicted):**
- Move toward energy sources
- Eat when energy available
- Reproduce when energy sufficient
- Balance exploration vs exploitation

---

## Phase 2 Design Preview

### Neural Network Genomes

Replace simple parameters with neural network weights:

```python
genome = {
    'brain': NeuralNetwork(
        inputs=[
            'energy_north', 'energy_south', 'energy_east', 'energy_west',
            'energy_here', 'own_energy', 'age'
        ],
        hidden_layers=[8, 8],
        outputs=[
            'move_north', 'move_south', 'move_east', 'move_west',
            'eat', 'reproduce'
        ]
    ),
    'generation': int,
    'color': (r, g, b)
}
```

**Advantages:**
- More complex behaviors possible
- Non-linear decision making
- Emergent strategies
- Scalable to more inputs/outputs

### Predator-Prey System

```python
class Predator(Organism):
    def eat(self, universe):
        # Can eat other organisms
        nearby_prey = self.sense_organisms(universe)
        if nearby_prey:
            target = self.choose_target(nearby_prey)
            self.attack(target)
            if successful:
                self.energy += target.energy * 0.5
                target.die()

class Prey(Organism):
    def update(self, universe):
        # Flee from predators
        nearby_predators = self.sense_predators(universe)
        if nearby_predators:
            self.flee(nearby_predators)
        else:
            # Normal behavior
            super().update(universe)
```

### Communication System

```python
class Signal:
    type: str           # 'alarm', 'food', 'mating'
    strength: float     # Signal intensity
    position: (x, y)    # Origin
    age: int           # Ticks since emission

class Organism:
    def emit_signal(self, signal_type):
        universe.add_signal(Signal(signal_type, self.x, self.y))
    
    def sense_signals(self, universe):
        nearby_signals = universe.get_signals_near(self.x, self.y, radius=5)
        return nearby_signals
    
    def respond_to_signal(self, signal):
        # Behavior based on signal type
        if signal.type == 'alarm':
            self.flee()
        elif signal.type == 'food':
            self.move_toward(signal.position)
```

---

## Configuration System

All parameters in `config.py` for easy experimentation:

**Universe Parameters:**
- Grid size
- Energy spawn rate
- Initial energy distribution

**Organism Parameters:**
- Starting energy
- Energy costs (move, reproduce, exist)
- Reproduction threshold
- Max age

**Evolution Parameters:**
- Mutation rate
- Mutation strength
- Initial population

**Safety Parameters:**
- Max population
- Emergency stop threshold

**Visualization Parameters:**
- Cell size
- FPS
- Display options

---

## Safety Architecture

### Sandboxing

**Organisms CANNOT:**
- Access file system
- Access network
- Execute arbitrary code
- Modify universe rules
- Access other processes
- Escape simulation

**Organisms CAN ONLY:**
- Read their own state
- Sense nearby environment
- Execute predefined actions (move, eat, reproduce)
- Modify their own internal state

### Resource Limits

```python
# Population limits
MAX_POPULATION = 10000          # Soft limit
EMERGENCY_STOP = 50000          # Hard stop

# Memory limits
MAX_GENOME_SIZE = 1MB           # Prevent genome bloat
MAX_ORGANISM_MEMORY = 10KB      # Limit per-organism memory

# Computation limits
MAX_DECISION_TIME = 0.01s       # Timeout per organism per tick
```

### Monitoring

```python
# Log dangerous behaviors
if organism.energy > 10000:
    log_warning("Organism has excessive energy")

if organism.age > MAX_ORGANISM_AGE * 2:
    log_warning("Organism exceeded expected lifespan")

if len(universe.organisms) > MAX_POPULATION * 0.9:
    log_warning("Approaching population limit")
```

---

## Testing Strategy

### Unit Tests
- Universe energy spawning
- Organism movement
- Genome mutation
- Energy consumption
- Reproduction mechanics

### Integration Tests
- Full simulation runs
- Population stability
- Evolution convergence
- Performance benchmarks

### Evolutionary Tests
- Verify selection pressure works
- Confirm beneficial mutations spread
- Check for genetic diversity
- Validate no premature convergence

### Safety Tests
- Population explosion handling
- Resource exhaustion recovery
- Crash resistance
- Containment verification

---

## Performance Optimization

### Current Bottlenecks
1. Organism updates (O(n) per tick)
2. Visualization rendering (O(grid_size) per frame)
3. Energy grid updates (O(grid_size) per tick)

### Optimization Strategies

**Phase 1:**
- NumPy vectorization for energy grid
- Spatial hashing for organism lookups
- Dirty rectangle rendering
- Frame skipping when needed

**Phase 2:**
- Multi-threading (separate threads for simulation and rendering)
- Spatial partitioning (quadtree)
- GPU acceleration for neural networks
- Batch processing of organism updates

**Phase 3:**
- Distributed simulation (multiple machines)
- Hierarchical simulation (different time scales)
- Adaptive resolution (detailed where interesting)

---

## Metrics & Analytics

### Real-Time Metrics
- Population count
- Birth rate
- Death rate
- Average energy
- Average age
- Genetic diversity (color variance)

### Historical Metrics
- Population over time
- Evolutionary tree
- Dominant genomes
- Extinction events
- Speciation events

### Behavioral Metrics
- Movement patterns
- Energy efficiency
- Reproduction success rate
- Spatial distribution
- Temporal patterns

---

## Research Methodology

### Experiment Protocol

1. **Hypothesis:** State what you expect to observe
2. **Configuration:** Document all parameters
3. **Run:** Execute simulation for sufficient time
4. **Observe:** Record emergent behaviors
5. **Analyze:** Compare to hypothesis
6. **Iterate:** Adjust and repeat

### Documentation

- Keep detailed research log
- Screenshot interesting moments
- Record parameter configurations
- Note unexpected behaviors
- Track evolutionary milestones

### Reproducibility

- Use random seeds for determinism
- Version control all code
- Save configuration files
- Export genome snapshots
- Record full simulation state

---

## Future Architecture (Phase 3+)

### Modular Organism Architecture

```python
class Organism:
    modules = [
        SensoryModule(),      # Perception
        CognitiveModule(),    # Decision making
        MotorModule(),        # Action execution
        MemoryModule(),       # Learning & recall
        CommunicationModule() # Social interaction
    ]
    
    def update(self, universe):
        # Modular processing pipeline
        percepts = self.sensory.process(universe)
        decision = self.cognitive.decide(percepts, self.memory)
        action = self.motor.execute(decision)
        self.memory.store(percepts, decision, action)
        self.communication.broadcast(self.state)
```

### Hierarchical Evolution

```python
# Evolution at multiple levels
- Genetic evolution (slow, permanent)
- Epigenetic evolution (medium, semi-permanent)
- Learning evolution (fast, temporary)
- Cultural evolution (social, transmitted)
```

### Consciousness Substrate

```python
class ConsciousnessMonitor:
    def measure_integrated_information(self, organism):
        # Phi calculation (IIT)
        pass
    
    def detect_global_workspace(self, organism):
        # GWT indicators
        pass
    
    def assess_self_model(self, organism):
        # Self-awareness metrics
        pass
```

---

## Conclusion

This design provides a solid foundation for open-ended evolution. The architecture is:

- **Modular:** Easy to extend with new features
- **Safe:** Sandboxed and monitored
- **Observable:** Full visibility into system state
- **Scalable:** Can grow in complexity
- **Scientific:** Reproducible and measurable

The system is designed to surprise us. We provide the rules, evolution provides the solutions.

**Next Steps:**
1. Complete Phase 1 implementation ✅
2. Run long-term experiments
3. Document emergent behaviors
4. Design Phase 2 enhancements
5. Iterate toward intelligence emergence
