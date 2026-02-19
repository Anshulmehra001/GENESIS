# GENESIS - Quick Start Guide

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Simulation

```bash
python main.py
```

## Controls

- **SPACE**: Pause/Resume simulation
- **R**: Reset universe (start over)
- **ESC**: Quit

## What You're Seeing

### Green Background
- Energy resources that organisms need to survive
- Brighter = more energy

### Colored Circles
- Living organisms
- Each color represents a genetic lineage
- Size indicates energy level

### Stats Panel (Bottom)
- **Tick**: Simulation time steps
- **Population**: Current number of living organisms
- **Births/Deaths**: Total organisms born and died
- **Avg Energy**: Average energy per organism
- **Total Energy**: Total energy in the world

## What to Watch For

### Phase 1: Initial Chaos (First 100 ticks)
- Organisms move randomly
- Many die quickly
- Population drops

### Phase 2: Adaptation (100-1000 ticks)
- Survivors have better genes
- Population stabilizes
- You'll see organisms cluster around energy

### Phase 3: Evolution (1000+ ticks)
- Different strategies emerge
- Some organisms move more, some less
- Color variations show genetic diversity
- Population cycles (boom and bust)

### Phase 4: Complexity (If you're lucky)
- Stable ecosystems form
- Multiple species coexist
- Emergent behaviors appear

## Experiments to Try

1. **Let it run overnight** - See what evolves after 100,000+ ticks
2. **Watch for extinction events** - Population crashes and recoveries
3. **Observe color patterns** - Successful genes spread (same colors)
4. **Look for strategies** - Do some organisms stay still? Move constantly?

## Next Steps

Once you see stable evolution:
1. We'll add more complex behaviors
2. Introduce predator/prey dynamics
3. Add communication between organisms
4. Implement learning (not just evolution)

## Troubleshooting

**Simulation runs too fast:**
- Edit `config.py`, increase `FPS` value

**Simulation runs too slow:**
- Edit `config.py`, decrease `GRID_WIDTH` and `GRID_HEIGHT`

**All organisms die immediately:**
- Edit `config.py`, increase `INITIAL_ENERGY_DISTRIBUTION`
- Or increase `ORGANISM_START_ENERGY`

**Population explodes:**
- This is interesting! Let it run and see what happens
- Safety limit will stop it at 50,000 organisms

---

**Remember:** You're watching evolution in real-time. Be patient. The most interesting behaviors take time to emerge.
