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

# Visualization
CELL_SIZE = 8
SHOW_ENERGY = True
SHOW_STATS = True
FPS = 30

# Safety
ENABLE_LOGGING = True
LOG_INTERVAL = 100  # Log stats every N ticks
EMERGENCY_STOP_POPULATION = 50000  # Hard stop if population explodes
