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

# Phase 2: Directional Sensing
ENABLE_DIRECTIONAL_SENSING = True
ENERGY_COST_TURN = 0.5  # Energy cost to change direction
VISION_CONE_ANGLE = 180  # Degrees of forward vision (180 = half circle)

# Phase 3: Multi-cellular
ENABLE_MULTICELLULAR = True
CELL_ADHESION_CHANCE = 0.01  # Chance for cells to stick together
MAX_ORGANISM_SIZE = 5  # Max cells in one organism

# Phase 3: Learning
ENABLE_LEARNING = True
LEARNING_RATE = 0.1

# Phase 2: Directional Sensing
ENABLE_DIRECTIONAL_SENSING = True
TURNING_ENERGY_COST = 0.1

# Phase 3: Social Structures
ENABLE_SOCIAL = True
KIN_RECOGNITION_THRESHOLD = 0.8

# Phase 3: Tool Use & Structures
ENABLE_STRUCTURES = True
ENABLE_TOOLS = True
STRUCTURE_BUILD_COST = 50
MAX_STRUCTURES = 500

# Phase 3: Problem Solving
ENABLE_PUZZLES = True
PUZZLE_SPAWN_CHANCE = 0.0001
MAX_PUZZLES = 10

# Phase 3: Social Hierarchy
ENABLE_HIERARCHY = True
CHALLENGE_ENERGY_COST = 10  # Genome similarity for kin recognition

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

# Persistence
ENABLE_AUTOSAVE = True
AUTOSAVE_INTERVAL = 1000  # Auto-save every N ticks
KEEP_AUTOSAVES = 5  # Number of autosaves to keep

# Phase 4: Cognitive Emergence
ENABLE_ABSTRACT_REASONING = True
ENABLE_LANGUAGE = True
ENABLE_SELF_AWARENESS = True
ENABLE_CREATIVITY = True
ENABLE_METACOGNITION = True

# Abstract Reasoning
PATTERN_RECOGNITION_MEMORY = 50  # How many observations to remember
CATEGORY_LIMIT = 20  # Max categories to form
CAUSAL_LEARNING_RATE = 0.1

# Language
LANGUAGE_INNOVATION_RATE = 0.01  # Chance to invent new symbol
LANGUAGE_LEARNING_RATE = 0.1  # Rate of learning from others
MAX_VOCABULARY_SIZE = 100
ENABLE_GRAMMAR = True

# Self-Awareness
ENABLE_SELF_RECOGNITION = True
ENABLE_THEORY_OF_MIND = True
REFLECTION_INTERVAL = 100  # Ticks between self-reflections
MAX_OTHER_MODELS = 10  # Max other organisms to model

# Creativity & Innovation
EXPLORATION_RATE = 0.3  # Balance exploration vs exploitation
PLAY_ENERGY_THRESHOLD = 0.7  # Energy level needed for play
NOVELTY_REWARD = 10  # Energy reward for novel behaviors
INNOVATION_DIFFUSION_RATE = 0.05  # How fast innovations spread

# Recursive Self-Improvement (Experimental - Disabled by default)
ENABLE_SELF_MODIFICATION = False  # DANGEROUS: Allow organisms to modify own code
SELF_MOD_SAFETY_CHECKS = True
SELF_MOD_ROLLBACK = True
MAX_MODIFICATIONS_PER_LIFETIME = 5

# Phase 5: AGI Emergence
ENABLE_GENERAL_INTELLIGENCE = True
ENABLE_AUTONOMOUS_GOALS = True
ENABLE_CONSCIOUSNESS_METRICS = True
ENABLE_ETHICAL_REASONING = True
ENABLE_NOVELTY_SEARCH = True

# General Problem Solving
PROBLEM_DIVERSITY = 5  # Number of problem domains
ENABLE_TRANSFER_LEARNING = True
ENABLE_ZERO_SHOT_LEARNING = True
ENABLE_META_LEARNING = True

# Goal Formation
MAX_GOALS_PER_ORGANISM = 10
GOAL_FORMATION_RATE = 0.01  # Chance per tick to form new goal
LONG_TERM_PLANNING_HORIZON = 1000  # Ticks

# Consciousness
CALCULATE_PHI = True  # Integrated Information Theory
GLOBAL_WORKSPACE_SIZE = 10
ATTENTION_MECHANISMS = True

# Ethics
FAIRNESS_LEARNING_RATE = 0.01
COOPERATION_LEARNING_RATE = 0.01
ENABLE_MORAL_EMOTIONS = True
ENABLE_REPUTATION = True

# Open-Ended Evolution
NOVELTY_REWARD_MULTIPLIER = 2.0  # Reward for novel behaviors
COMPLEXITY_TRACKING = True
DIVERSITY_MAINTENANCE = True
EXTINCTION_RESISTANCE = True
