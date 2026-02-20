#!/usr/bin/env python3
"""
Neural Architecture Search - Evolve networks to solve real problems
This is where we can achieve something actually useful and new
"""

import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neural_architecture_search import NASEvolution

def load_mnist_sample():
    """Load a small sample of MNIST for testing"""
    print("📊 Loading MNIST dataset...")
    
    try:
        from sklearn.datasets import load_digits
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        
        # Load digits dataset (8x8 images, 10 classes)
        digits = load_digits()
        X = digits.data
        y = digits.target
        
        # Normalize
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        print(f"✅ Loaded {len(X_train)} training samples, {len(X_test)} test samples")
        print(f"   Input size: {X.shape[1]}, Output classes: {len(np.unique(y))}")
        
        return X_train, y_train, X_test, y_test
    
    except ImportError:
        print("❌ scikit-learn not installed")
        print("   Install: pip install scikit-learn")
        sys.exit(1)

def create_simple_dataset():
    """Create simple XOR-like problem for testing"""
    print("📊 Creating simple test dataset...")
    
    np.random.seed(42)
    
    # Generate data
    n_samples = 200
    X = np.random.randn(n_samples, 2)
    y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)  # XOR
    
    # Split
    split = int(0.7 * n_samples)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    print(f"✅ Created {len(X_train)} training samples, {len(X_test)} test samples")
    return X_train, y_train, X_test, y_test

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         Neural Architecture Search (NAS)                  ║
    ║                                                           ║
    ║     Evolve neural networks to solve real problems        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Load dataset
    use_mnist = '--mnist' in sys.argv
    
    if use_mnist:
        X_train, y_train, X_test, y_test = load_mnist_sample()
    else:
        X_train, y_train, X_test, y_test = create_simple_dataset()
    
    input_size = X_train.shape[1]
    output_size = len(np.unique(y_train))
    
    # Initialize NAS
    print(f"\n🧬 Initializing Neural Architecture Search...")
    print(f"   Population size: 20")
    print(f"   Input size: {input_size}")
    print(f"   Output classes: {output_size}")
    
    nas = NASEvolution(input_size, output_size, population_size=20)
    
    # Evolution loop
    num_generations = 50
    print(f"\n🚀 Starting evolution for {num_generations} generations...\n")
    
    try:
        for gen in range(num_generations):
            # Evaluate population
            nas.evaluate_population(X_train, y_train, X_test, y_test)
            
            # Get stats
            stats = nas.get_stats()
            
            # Print progress
            if gen % 5 == 0:
                print(f"Generation {gen:3d} | "
                      f"Best Accuracy: {stats['best_accuracy']:.3f} | "
                      f"Avg Fitness: {stats['avg_fitness']:.3f} | "
                      f"Avg Layers: {stats['avg_layers']:.1f}")
            
            # Evolve next generation
            nas.evolve_generation()
        
        # Final evaluation
        print("\n" + "="*60)
        print("EVOLUTION COMPLETE")
        print("="*60)
        
        best = nas.get_best_architecture()
        print(f"\n🏆 Best Architecture Found:")
        print(f"   Accuracy: {best.accuracy:.3f}")
        print(f"   Fitness: {best.fitness:.3f}")
        print(f"   Layers: {best.num_layers}")
        print(f"   Layer sizes: {best.layer_sizes}")
        print(f"   Activations: {best.activations}")
        print(f"   Skip connections: {len(best.skip_connections)}")
        print(f"   Complexity: {best.complexity:,} parameters")
        
        # Test on full test set
        correct = 0
        for x, y in zip(X_test, y_test):
            pred = best.forward(x)
            if np.argmax(pred) == y:
                correct += 1
        
        final_accuracy = correct / len(X_test)
        print(f"\n📊 Final Test Accuracy: {final_accuracy:.3f}")
        
        # Save best architecture
        import json
        with open('best_architecture.json', 'w') as f:
            json.dump(best.to_dict(), f, indent=2)
        print(f"\n💾 Saved best architecture to: best_architecture.json")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Evolution interrupted by user")
        stats = nas.get_stats()
        print(f"   Best accuracy so far: {stats['best_accuracy']:.3f}")

if __name__ == "__main__":
    main()
