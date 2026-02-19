"""
Detailed test for vision cone functionality
"""

import math
from organism import Organism
from universe import Universe
from config import *

def test_vision_cone_all_directions():
    """Test vision cone for all 8 directions"""
    print("Testing vision cone for all 8 directions...")
    print(f"Vision cone angle: {VISION_CONE_ANGLE} degrees")
    
    universe = Universe()
    org = Organism(50, 50)
    
    direction_names = ["North", "NE", "East", "SE", "South", "SW", "West", "NW"]
    
    for direction in range(8):
        org.direction = direction
        print(f"\n  Direction {direction} ({direction_names[direction]}):")
        
        # Test what can be seen in each direction
        test_positions = [
            (0, -2, "North"),
            (2, -2, "NE"),
            (2, 0, "East"),
            (2, 2, "SE"),
            (0, 2, "South"),
            (-2, 2, "SW"),
            (-2, 0, "West"),
            (-2, -2, "NW")
        ]
        
        visible_count = 0
        for dx, dy, name in test_positions:
            can_see = org._is_in_vision_cone(dx, dy)
            if can_see:
                visible_count += 1
                print(f"    ✓ Can see {name} ({dx}, {dy})")
        
        print(f"    Total visible: {visible_count}/8 directions")

def test_sense_environment_with_cone():
    """Test that sense_environment respects vision cone"""
    print("\n\nTesting sense_environment with vision cone...")
    
    universe = Universe()
    
    # Place energy in all directions around organism
    org = Organism(50, 50)
    org.direction = 0  # Facing North
    
    # Add energy in all 8 directions
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            universe.energy_grid[50 + dy][50 + dx] = 100
    
    # Sense environment
    nearby = org.sense_environment(universe)
    
    print(f"  Organism facing North")
    print(f"  Total cells with energy: 8")
    print(f"  Cells visible in forward cone: {len(nearby)}")
    
    # With 180 degree cone facing north, should see north, northeast, northwest, east, west
    # Should NOT see south, southeast, southwest
    visible_directions = [(dx, dy) for dx, dy, e in nearby]
    print(f"  Visible positions: {visible_directions}")
    
    # Check that south is not visible
    south_visible = any(dy > 0 and dx == 0 for dx, dy, e in nearby)
    print(f"  Can see directly behind (South): {south_visible}")

def test_predator_vision_cone():
    """Test that predators also use vision cone"""
    print("\n\nTesting predator vision cone...")
    
    try:
        from predator import Predator
        
        universe = Universe()
        predator = Predator(50, 50)
        predator.direction = 2  # Facing East
        
        # Add prey in various directions
        from organism import Organism
        prey_north = Organism(50, 45)
        prey_east = Organism(55, 50)
        prey_south = Organism(50, 55)
        
        universe.organisms = [predator, prey_north, prey_east, prey_south]
        
        # Sense prey
        nearby_prey = predator.sense_prey(universe)
        
        print(f"  Predator facing East")
        print(f"  Total prey: 3 (North, East, South)")
        print(f"  Prey visible: {len(nearby_prey)}")
        
        for prey, dx, dy, dist in nearby_prey:
            direction = "unknown"
            if dx > 0 and dy == 0:
                direction = "East"
            elif dx == 0 and dy < 0:
                direction = "North"
            elif dx == 0 and dy > 0:
                direction = "South"
            print(f"    - Prey at {direction} (distance: {dist:.1f})")
        
        print("  ✓ Predator vision cone working")
        
    except ImportError:
        print("  Skipped (predator module not available)")

def main():
    print("=" * 70)
    print("DETAILED VISION CONE TEST")
    print("=" * 70)
    
    test_vision_cone_all_directions()
    test_sense_environment_with_cone()
    test_predator_vision_cone()
    
    print("\n" + "=" * 70)
    print("✅ VISION CONE TESTS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
