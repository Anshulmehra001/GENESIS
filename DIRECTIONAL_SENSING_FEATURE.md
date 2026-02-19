# Directional Sensing Feature

## Overview
Organisms now have a facing direction and can only see in a forward vision cone. Turning to face a new direction costs energy, adding strategic depth to movement decisions.

## Implementation Details

### 1. Facing Direction
- Each organism has a `direction` attribute (0-7 representing 8 compass directions)
- Directions: 0=N, 1=NE, 2=E, 3=SE, 4=S, 5=SW, 6=W, 7=NW
- Direction is randomly initialized at birth
- Direction updates automatically when the organism moves

### 2. Vision Cone
- Organisms can only see within a forward-facing cone
- Default cone angle: 180 degrees (half circle)
- Vision cone is applied to:
  - Energy sensing (`sense_environment`)
  - Organism detection (`sense_organisms`)
  - Predator prey detection (`sense_prey`)
- Organisms cannot see directly behind them

### 3. Turning Cost
- Changing direction costs energy: `ENERGY_COST_TURN = 0.5`
- Moving straight ahead: costs only `ENERGY_COST_MOVE = 1.0`
- Moving in a new direction: costs `ENERGY_COST_MOVE + ENERGY_COST_TURN = 1.5`
- This encourages organisms to move in straight lines when possible

### 4. Neural Network Integration
- Direction is provided as an input to the neural network (normalized 0-1)
- Allows organisms to learn direction-aware behaviors
- Neural networks can evolve strategies that consider current facing direction

### 5. Visualization
- A white line extends from each organism showing its facing direction
- Line length scales with organism size
- Makes it easy to observe directional behaviors in the simulation

## Configuration

New config parameters in `config.py`:

```python
# Phase 2: Directional Sensing
ENABLE_DIRECTIONAL_SENSING = True
ENERGY_COST_TURN = 0.5  # Energy cost to change direction
VISION_CONE_ANGLE = 180  # Degrees of forward vision (180 = half circle)
```

## Evolutionary Implications

### Strategic Movement
- Organisms must balance exploration vs. energy efficiency
- Turning frequently to scan environment costs more energy
- Moving in straight lines is more efficient but may miss opportunities

### Predator-Prey Dynamics
- Prey can escape by moving behind predators (outside vision cone)
- Predators must face their prey to see and hunt them
- Creates more realistic chase dynamics

### Emergent Behaviors
Expected to see evolution of:
- Efficient scanning patterns (sweep head back and forth)
- Pursuit strategies (face target while moving)
- Evasion tactics (move perpendicular to predator's facing direction)
- Group coordination (organisms facing different directions for 360° coverage)

## Testing

Run the test suite to verify functionality:

```bash
python test_directional_sensing.py
python test_vision_cone_detailed.py
```

All tests pass, confirming:
- ✓ Direction initialization
- ✓ Vision cone restricts sensing
- ✓ Turning costs energy
- ✓ Direction updates with movement
- ✓ Neural network receives direction input
- ✓ Predators use vision cone

## Future Enhancements

Potential improvements:
1. Variable vision cone angles (narrow for focused vision, wide for peripheral)
2. Separate turning speed (fast turn = more energy, slow turn = less energy)
3. Head vs. body direction (look without moving)
4. Blind spots and peripheral vision quality
5. Evolution of vision cone angle as a genetic trait

## Impact on Simulation

This feature adds significant complexity to the simulation:
- More realistic sensory limitations
- Strategic trade-offs in movement
- Richer predator-prey interactions
- Foundation for more sophisticated spatial awareness

The directional sensing system is a key step toward organisms that navigate their environment intelligently rather than omnisciently.
