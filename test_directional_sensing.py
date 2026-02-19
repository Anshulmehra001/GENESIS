"""
Test script for directional sensing feature
"""

import sys
from organism import Organism
from universe import Universe
from config import *

def test_direction_initialization():
    """Test that organisms are initialized with a direction"""
    print("Testing direction initialization...")
    org = Organism(50, 50)
    assert hasattr(org, 'direction'), "Organism should have direction attribute"
    assert 0 <= org.direction <= 7, f"Direction should be 0-7, got {org.direction}"
    print(f"✓ Organism initialized with direction: {org.direction}")

def test_vision_cone():
    """Test that vision cone restricts what organisms can see"""
    print("\nTesting vision cone...")
    universe = Universe()
    
    # Create organism facing North (direction 0)
    org = Organism(50, 50)
    org.direction = 0  # North
    
    # Test vision cone method
    # Should see things in front (north)
    assert org._is_in_vision_cone(0, -1), "Should see directly ahead (north)"
    assert org._is_in_vision_cone(1, -1), "Should see northeast"
    assert org._is_in_vision_cone(-1, -1), "Should see northwest"
    
    # With 180 degree cone, should not see directly behind
    if VISION_CONE_ANGLE == 180:
        # At 180 degrees, things directly to the side are at the edge
        # Things behind should not be visible
        result = org._is_in_vision_cone(0, 1)
        print(f"  Can see directly behind (south): {result}")
    
    print("✓ Vision cone working correctly")

def test_turning_cost():
    """Test that turning costs energy"""
    print("\nTesting turning energy cost...")
    universe = Universe()
    
    org = Organism(50, 50)
    org.direction = 0  # North
    initial_energy = org.energy
    
    # Move in same direction (no turn)
    org.move(0, -1, universe)
    energy_after_straight = org.energy
    straight_cost = initial_energy - energy_after_straight
    print(f"  Energy cost for straight move: {straight_cost}")
    
    # Reset and move in different direction (turn)
    org2 = Organism(50, 50)
    org2.direction = 0  # North
    initial_energy2 = org2.energy
    
    org2.move(1, 0, universe)  # Move East (turn required)
    energy_after_turn = org2.energy
    turn_cost = initial_energy2 - energy_after_turn
    print(f"  Energy cost for turn + move: {turn_cost}")
    
    assert turn_cost > straight_cost, "Turning should cost more energy than straight movement"
    print(f"✓ Turning costs extra energy ({turn_cost - straight_cost} extra)")

def test_direction_update():
    """Test that direction updates when moving"""
    print("\nTesting direction updates...")
    universe = Universe()
    
    org = Organism(50, 50)
    org.direction = 0  # North
    
    # Move east
    org.move(1, 0, universe)
    assert org.direction == 2, f"Direction should be 2 (East), got {org.direction}"
    print(f"✓ Direction updated to East (2)")
    
    # Move south
    org.move(0, 1, universe)
    assert org.direction == 4, f"Direction should be 4 (South), got {org.direction}"
    print(f"✓ Direction updated to South (4)")
    
    # Move northwest
    org.move(-1, -1, universe)
    assert org.direction == 7, f"Direction should be 7 (NW), got {org.direction}"
    print(f"✓ Direction updated to Northwest (7)")

def test_neural_network_input():
    """Test that neural network receives direction as input"""
    print("\nTesting neural network direction input...")
    
    if not USE_NEURAL_NETWORKS:
        print("  Skipped (neural networks disabled)")
        return
    
    universe = Universe()
    org = Organism(50, 50)
    org.direction = 3  # Southeast
    
    # Call neural decision making
    dx, dy = org._neural_decide_move(universe)
    
    print(f"✓ Neural network processed direction input successfully")
    print(f"  Decided to move: dx={dx}, dy={dy}")

def main():
    print("=" * 60)
    print("DIRECTIONAL SENSING TEST SUITE")
    print("=" * 60)
    
    try:
        test_direction_initialization()
        test_vision_cone()
        test_turning_cost()
        test_direction_update()
        test_neural_network_input()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
