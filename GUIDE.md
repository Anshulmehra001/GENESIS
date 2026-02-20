# GENESIS - Complete Guide

## What Is This?

Digital organisms that evolve, learn, communicate, and develop complex behaviors through natural selection.

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run with visualization
python run.py

# Run HEADLESS (10x faster, for long experiments)
python run.py --headless

# Resume from save
python run.py final_save.pkl

# Resume headless
python run.py --headless final_save.pkl
```

## For Long-Term Experiments (Million+ Ticks)

**On average laptop:**

1. **Use headless mode** - 10x faster
```bash
python run.py --headless
```

2. **Enable performance mode** in `src/config.py`:
```python
PERFORMANCE_MODE = True  # Disables expensive features
```

3. **Run overnight** - auto-saves every 1000 ticks

**Time estimate:** 10-20 hours for 1 million ticks

## Controls

- **SPACE**: Pause/Resume
- **S**: Save manually
- **R**: Reset
- **ESC**: Quit (auto-saves)

## What's Implemented

**Phase 1: Foundation**
- Self-replicating organisms
- Genetic evolution
- Energy-based ecosystem

**Phase 2: Evolution**
- Neural network brains
- Predator-prey dynamics
- Communication signals
- Memory system
- Directional sensing

**Phase 3: Emergence**
- Multi-cellular organisms
- Social hierarchies
- Tool use and structures
- Problem-solving puzzles
- Kin recognition

**Phase 4: Cognition**
- Abstract reasoning (pattern recognition, causal models)
- Language emergence (symbols, grammar, meaning)
- Self-awareness (self-recognition, theory of mind)
- Creativity (novel behaviors, exploration, play)

## Configuration

Edit `src/config.py` to enable/disable features and adjust parameters.

## File Structure

```
src/          - All source code
docs/         - Documentation
tests/        - Test files
saves/        - Saved simulations
run.py        - Entry point
```

## Is This Real AI?

No. It's a simulation that models intelligent-looking behaviors. The organisms follow algorithms, they don't genuinely think or feel.

## What Can You Do?

- Run long-term experiments (saves persist)
- Observe emergent behaviors
- Modify parameters and see what happens
- Learn about evolution and AI concepts
- Use as portfolio/educational project

## Limitations

- Not genuine AGI
- Computational simulation, not consciousness
- Educational/research tool, not breakthrough technology

## Next Steps

1. Run for extended periods (weeks/months)
2. Document interesting emergent behaviors
3. Experiment with different parameters
4. Apply to practical problems (optimization, game AI, etc.)

---

**Reality Check:** This is a learning project that implements known AI concepts. It's interesting and educational, but not revolutionary research.
