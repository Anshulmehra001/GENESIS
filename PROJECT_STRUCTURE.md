# GENESIS Project Structure

This document describes the organization of the GENESIS Digital Biosphere project.

## Directory Structure

```
genesis-digital-biosphere/
│
├── src/                          # Source Code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main simulation loop and entry point
│   ├── config.py                # All configuration parameters
│   ├── universe.py              # Universe/world management
│   ├── organism.py              # Base organism implementation
│   ├── visualizer.py            # Real-time visualization with pygame
│   │
│   ├── neural_network.py        # Neural network brains (Phase 2)
│   ├── predator.py              # Predator organisms (Phase 2)
│   ├── signal.py                # Communication signals (Phase 2)
│   ├── directional_sensing.py   # Vision cones and sensing (Phase 2)
│   │
│   ├── structures.py            # Environmental structures (Phase 3)
│   ├── problem_solving.py       # Puzzles and challenges (Phase 3)
│   ├── social_hierarchy.py      # Social systems (Phase 3)
│   └── organism_extensions.py   # Extension methods (Phase 3)
│
├── docs/                         # Documentation
│   ├── README.md                # Documentation index
│   ├── START_HERE.md            # Getting started guide
│   ├── QUICKSTART.md            # Quick reference
│   ├── VISION.md                # Project vision and philosophy
│   ├── ROADMAP.md               # Development roadmap
│   ├── RESEARCH_LOG.md          # Research observations
│   ├── TASK_STATUS_SUMMARY.md   # Task completion status
│   ├── PHASE_2_3_COMPLETE.md    # Phase 2 & 3 summary
│   ├── PHASE_2_3_IMPLEMENTATION.md  # Implementation details
│   ├── PHASE2_3_FEATURES.md     # Feature specifications
│   └── DIRECTIONAL_SENSING_FEATURE.md  # Vision system details
│
├── tests/                        # Test Files
│   ├── README.md                # Test documentation
│   ├── test_directional_sensing.py
│   └── test_vision_cone_detailed.py
│
├── .kiro/                        # Kiro IDE Configuration
│   └── specs/genesis-digital-biosphere/
│       ├── requirements.md      # Detailed requirements
│       ├── design.md            # System architecture
│       └── tasks.md             # Implementation tasks
│
├── run.py                        # Entry point script
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview
├── PROJECT_STRUCTURE.md          # This file
└── .gitignore                    # Git ignore rules

```

## Key Files

### Entry Points
- **run.py** - Main entry point to start the simulation
- **src/main.py** - Core simulation loop

### Configuration
- **src/config.py** - All simulation parameters and feature flags

### Core Systems
- **src/organism.py** - Organism behavior and lifecycle
- **src/universe.py** - World management, energy, structures
- **src/visualizer.py** - Real-time visualization

### Phase 2 Features (Evolution & Complexity)
- **src/neural_network.py** - Brain implementation
- **src/predator.py** - Predator behavior
- **src/signal.py** - Communication system
- **src/directional_sensing.py** - Vision and sensing

### Phase 3 Features (Emergence & Intelligence)
- **src/structures.py** - Buildings and tools
- **src/problem_solving.py** - Puzzles
- **src/social_hierarchy.py** - Social systems
- **src/organism_extensions.py** - Additional organism methods

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run simulation
python run.py
```

## Development Workflow

1. Check **docs/ROADMAP.md** for project direction
2. Review **.kiro/specs/genesis-digital-biosphere/tasks.md** for tasks
3. Modify **src/config.py** to enable/disable features
4. Edit source files in **src/**
5. Add tests in **tests/**
6. Document observations in **docs/RESEARCH_LOG.md**

## Documentation

All documentation is in the **docs/** directory. Start with **docs/START_HERE.md** for an introduction.

## Testing

Tests are in the **tests/** directory. Run with:
```bash
python -m pytest tests/
```

## Version

Current version: 0.3.0 (Phase 1, 2, 3 Complete)
