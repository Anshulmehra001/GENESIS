"""
GENESIS - Digital Biosphere
The first truly open-ended artificial life system

Run this to start the simulation and watch evolution unfold.
"""

import random
from universe import Universe
from organism import Organism
from visualizer import Visualizer
from config import *

def initialize_universe():
    """Create universe and spawn initial organisms"""
    universe = Universe()
    
    print("🌍 Initializing GENESIS Digital Biosphere...")
    print(f"   Grid: {GRID_WIDTH}x{GRID_HEIGHT}")
    print(f"   Initial organisms: {INITIAL_ORGANISMS}")
    print(f"   Mutation rate: {MUTATION_RATE * 100}%")
    print(f"   Neural networks: {USE_NEURAL_NETWORKS}")
    print(f"   Predators enabled: {ENABLE_PREDATORS}")
    print(f"   Communication enabled: {ENABLE_COMMUNICATION}")
    print(f"   Multi-cellular enabled: {ENABLE_MULTICELLULAR}")
    print()
    
    # Spawn initial prey organisms
    for _ in range(INITIAL_ORGANISMS):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        organism = Organism(x, y)
        universe.add_organism(organism)
    
    # Spawn initial predators
    if ENABLE_PREDATORS:
        from predator import Predator
        for _ in range(INITIAL_PREDATORS):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            predator = Predator(x, y)
            universe.add_organism(predator)
    
    print("✅ Universe initialized")
    print("🧬 Evolution begins NOW\n")
    
    return universe

def log_stats(universe):
    """Print statistics to console"""
    stats = universe.get_stats()
    
    print(f"[Tick {stats['tick']:6d}] "
          f"Pop: {stats['population']:4d} | "
          f"Births: {stats['total_births']:5d} | "
          f"Deaths: {stats['total_deaths']:5d} | "
          f"Avg Energy: {stats['avg_organism_energy']:6.1f}")

def main():
    """Main simulation loop"""
    universe = initialize_universe()
    visualizer = Visualizer(universe)
    
    running = True
    
    try:
        while running:
            # Handle user input
            event_result = visualizer.handle_events()
            
            if event_result == False:
                running = False
                break
            elif event_result == 'reset':
                print("\n🔄 Resetting universe...\n")
                universe = initialize_universe()
                visualizer.universe = universe
                continue
            
            # Update simulation (if not paused)
            if not visualizer.is_paused():
                success = universe.update()
                
                if not success:
                    print("\n⚠️ Simulation stopped due to safety limits")
                    running = False
                    break
                
                # Log stats periodically
                if ENABLE_LOGGING and universe.tick % LOG_INTERVAL == 0:
                    log_stats(universe)
                
                # Check for extinction
                if len(universe.organisms) == 0:
                    print(f"\n💀 EXTINCTION at tick {universe.tick}")
                    print("   All organisms have died.")
                    print("   Press R to reset or ESC to quit")
            
            # Render visualization
            visualizer.render()
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Simulation interrupted by user")
    
    finally:
        # Final statistics
        stats = universe.get_stats()
        print("\n" + "="*60)
        print("FINAL STATISTICS")
        print("="*60)
        print(f"Total ticks:        {stats['tick']}")
        print(f"Final population:   {stats['population']}")
        print(f"Peak population:    {stats['peak_population']}")
        print(f"Total births:       {stats['total_births']}")
        print(f"Total deaths:       {stats['total_deaths']}")
        print(f"Energy consumed:    {stats['total_energy_consumed']:.0f}")
        print("="*60)
        
        visualizer.close()
        print("\n👋 Simulation ended. Thank you for exploring GENESIS.")

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                    G E N E S I S                          ║
    ║                                                           ║
    ║         Digital Biosphere - Open-Ended Evolution          ║
    ║                                                           ║
    ║  "We are not creating AI. We are creating the conditions  ║
    ║           for AI to create itself."                       ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    main()
