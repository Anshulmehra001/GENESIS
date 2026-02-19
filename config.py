# GENESIS Configuration

# Universe Parameters
GRID_WIDTH = 100
GRID_HEIGHT = 100
INITIAL_ENERGY_DISTRIBUTION = 0.3  # 30% of cells start with energy

# Energy System
ENERGY_SPAWN_RATE = 0.01  # Probability of energy appearing per cell per tick
ENERGY_AMOUNT = 100  # Energy units per resource
MAX_ENERGY_PER_CELL = 500

# Organism Parameters
INITIAL_ORGANISMS = 10
ORGANISM_START_ENERGY = 200
ENERGY_COST_MOVE = 1
ENERGY_COST_REPLICATE = 150
ENERGY_COST_ALIVE = 0.5  # Energy cost per tick just to exist
MIN_ENERGY_TO_REPLICATE = 200

# Evolution Parameters
MUTATION_RATE = 0.1  # 10% chance of mutation during replication
MUTATION_STRENGTH = 0.2  # How much genes can change

# Simulation Parameters
MAX_POPULATION = 10000  # Safety limit
TICKS_PER_SECOND = 10
MAX_ORGANISM_AGE = 1000  # Organisms die of old age

# Phase 2: Neural Networks
USE_NEURAL_NETWORKS = True  # Use neural networks instead of simple genomes
NEURAL_HIDDEN_LAYERS = [8, 8]  # Hidden layer sizes
NEURAL_MUTATION_RATE = 0.1
NEURAL_MUTATION_STRENGTH = 0.2

# Phase 2: Predator-Prey
ENABLE_PREDATORS = True
INITIAL_PREDATORS = 2
PREDATOR_SPAWN_CHANCE = 0.001  # Chance per tick to spawn predator

# Phase 2: Communication
ENABLE_COMMUNICATION = True
SIGNAL_COST = 5  # Energy cost to emit signal
MAX_SIGNALS = 1000  # Maximum signals in universe

# Phase 2: Memory
ENABLE_MEMORY = True
MEMORY_SIZE = 10  # Number of locations to remember
VISION_RANGE = 5  # How far organisms can see

# Phase 3: Multi-cellular
ENABLE_MULTICELLULAR = True
CELL_ADHESION_CHANCE = 0.01  # Chance for cells to stick together
MAX_ORGANISM_SIZE = 5  # Max cells in one organism

# Phase 3: Learning
ENABLE_LEARNING = True
LEARNING_RATE = 0.1

# Phase 3: Social Structures
ENABLE_SOCIAL = True
KIN_RECOGNITION_THRESHOLD = 0.8  # Genome similarity for kin recognition

# Visualization
CELL_SIZE = 8
SHOW_ENERGY = True
SHOW_STATS = True
SHOW_SIGNALS = True
SHOW_MEMORY = False
FPS = 30

# Safety
ENABLE_LOGGING = True
LOG_INTERVAL = 100  # Log stats every N ticks
EMERGENCY_STOP_POPULATION = 50000  # Hard stop if population explodes
