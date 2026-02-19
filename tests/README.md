# GENESIS Tests

Test files for the GENESIS Digital Biosphere.

## Available Tests

- **test_directional_sensing.py** - Tests for vision cone and directional sensing
- **test_vision_cone_detailed.py** - Detailed vision cone tests

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_directional_sensing.py

# Run with verbose output
python -m pytest -v tests/
```

## Test Coverage

Current test coverage focuses on:
- Directional sensing and vision cones
- Organism perception systems

## Adding Tests

When adding new features, please add corresponding tests to ensure functionality.
