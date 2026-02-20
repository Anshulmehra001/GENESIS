"""
Neural Architecture Search (NAS)
Organisms evolve neural network architectures to solve real problems
"""

import random
import numpy as np
from collections import deque

class NetworkArchitecture:
    """Represents an evolvable neural network architecture"""
    
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        
        # Architecture genes
        self.num_layers = random.randint(1, 5)
        self.layer_sizes = [random.randint(4, 64) for _ in range(self.num_layers)]
        self.activations = [random.choice(['relu', 'tanh', 'sigmoid']) 
                           for _ in range(self.num_layers)]
        self.dropout_rates = [random.uniform(0, 0.5) for _ in range(self.num_layers)]
        
        # Skip connections (like ResNet)
        self.skip_connections = []
        for i in range(self.num_layers):
            if random.random() < 0.3 and i > 0:
                skip_from = random.randint(0, i-1)
                self.skip_connections.append((skip_from, i))
        
        # Performance tracking
        self.fitness = 0.0
        self.accuracy = 0.0
        self.training_time = 0.0
        self.complexity = self.calculate_complexity()
        
        # Build actual network
        self.weights = self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize network weights"""
        weights = []
        
        prev_size = self.input_size
        for layer_size in self.layer_sizes:
            # Xavier initialization
            limit = np.sqrt(6.0 / (prev_size + layer_size))
            W = np.random.uniform(-limit, limit, (prev_size, layer_size))
            b = np.zeros(layer_size)
            weights.append((W, b))
            prev_size = layer_size
        
        # Output layer
        limit = np.sqrt(6.0 / (prev_size + self.output_size))
        W = np.random.uniform(-limit, limit, (prev_size, self.output_size))
        b = np.zeros(self.output_size)
        weights.append((W, b))
        
        return weights
    
    def forward(self, x):
        """Forward pass through network"""
        activations = [x]
        
        for i, ((W, b), activation_fn) in enumerate(zip(self.weights[:-1], self.activations)):
            # Linear transformation
            z = np.dot(activations[-1], W) + b
            
            # Apply activation
            if activation_fn == 'relu':
                a = np.maximum(0, z)
            elif activation_fn == 'tanh':
                a = np.tanh(z)
            else:  # sigmoid
                a = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
            
            # Apply dropout (only during training)
            # For simplicity, we skip dropout in inference
            
            # Check for skip connections
            for skip_from, skip_to in self.skip_connections:
                if skip_to == i and len(activations[skip_from]) == len(a):
                    a = a + activations[skip_from]
            
            activations.append(a)
        
        # Output layer (no activation for regression, softmax for classification)
        W, b = self.weights[-1]
        output = np.dot(activations[-1], W) + b
        
        # Softmax for classification
        exp_output = np.exp(output - np.max(output))
        output = exp_output / np.sum(exp_output)
        
        return output
    
    def calculate_complexity(self):
        """Calculate network complexity (number of parameters)"""
        complexity = 0
        prev_size = self.input_size
        
        for layer_size in self.layer_sizes:
            complexity += prev_size * layer_size + layer_size
            prev_size = layer_size
        
        complexity += prev_size * self.output_size + self.output_size
        return complexity
    
    def mutate(self, mutation_rate=0.3):
        """Mutate architecture"""
        mutated = NetworkArchitecture(self.input_size, self.output_size)
        
        # Copy current architecture
        mutated.num_layers = self.num_layers
        mutated.layer_sizes = self.layer_sizes.copy()
        mutated.activations = self.activations.copy()
        mutated.dropout_rates = self.dropout_rates.copy()
        mutated.skip_connections = self.skip_connections.copy()
        
        # Mutate number of layers
        if random.random() < mutation_rate:
            if random.random() < 0.5 and mutated.num_layers > 1:
                # Remove layer
                idx = random.randint(0, mutated.num_layers - 1)
                mutated.layer_sizes.pop(idx)
                mutated.activations.pop(idx)
                mutated.dropout_rates.pop(idx)
                mutated.num_layers -= 1
            elif mutated.num_layers < 5:
                # Add layer
                idx = random.randint(0, mutated.num_layers)
                mutated.layer_sizes.insert(idx, random.randint(4, 64))
                mutated.activations.insert(idx, random.choice(['relu', 'tanh', 'sigmoid']))
                mutated.dropout_rates.insert(idx, random.uniform(0, 0.5))
                mutated.num_layers += 1
        
        # Mutate layer sizes
        if random.random() < mutation_rate:
            idx = random.randint(0, mutated.num_layers - 1)
            mutated.layer_sizes[idx] = max(4, mutated.layer_sizes[idx] + random.randint(-16, 16))
        
        # Mutate activations
        if random.random() < mutation_rate:
            idx = random.randint(0, mutated.num_layers - 1)
            mutated.activations[idx] = random.choice(['relu', 'tanh', 'sigmoid'])
        
        # Mutate skip connections
        if random.random() < mutation_rate:
            if random.random() < 0.5 and mutated.skip_connections:
                # Remove skip connection
                mutated.skip_connections.pop(random.randint(0, len(mutated.skip_connections) - 1))
            elif mutated.num_layers > 1:
                # Add skip connection
                i = random.randint(1, mutated.num_layers - 1)
                skip_from = random.randint(0, i - 1)
                mutated.skip_connections.append((skip_from, i))
        
        # Rebuild weights
        mutated.weights = mutated._initialize_weights()
        mutated.complexity = mutated.calculate_complexity()
        
        return mutated
    
    def to_dict(self):
        """Serialize architecture"""
        return {
            'num_layers': self.num_layers,
            'layer_sizes': self.layer_sizes,
            'activations': self.activations,
            'dropout_rates': self.dropout_rates,
            'skip_connections': self.skip_connections,
            'fitness': self.fitness,
            'accuracy': self.accuracy,
            'complexity': self.complexity
        }

class NASEvolution:
    """Evolutionary Neural Architecture Search"""
    
    def __init__(self, input_size, output_size, population_size=20):
        self.input_size = input_size
        self.output_size = output_size
        self.population_size = population_size
        
        # Population of architectures
        self.population = [NetworkArchitecture(input_size, output_size) 
                          for _ in range(population_size)]
        
        # Evolution tracking
        self.generation = 0
        self.best_architecture = None
        self.best_fitness = 0.0
        self.fitness_history = []
    
    def evaluate_population(self, X_train, y_train, X_val, y_val):
        """Evaluate all architectures on dataset"""
        for arch in self.population:
            # Simple training: just evaluate on validation set
            # (Real training would use gradient descent)
            correct = 0
            total = len(X_val)
            
            for x, y in zip(X_val, y_val):
                prediction = arch.forward(x)
                predicted_class = np.argmax(prediction)
                if predicted_class == y:
                    correct += 1
            
            accuracy = correct / total
            arch.accuracy = accuracy
            
            # Fitness = accuracy - complexity penalty
            complexity_penalty = arch.complexity / 10000.0
            arch.fitness = accuracy - 0.1 * complexity_penalty
        
        # Update best
        best = max(self.population, key=lambda a: a.fitness)
        if best.fitness > self.best_fitness:
            self.best_fitness = best.fitness
            self.best_architecture = best
        
        self.fitness_history.append(self.best_fitness)
    
    def evolve_generation(self):
        """Create next generation"""
        # Sort by fitness
        self.population.sort(key=lambda a: a.fitness, reverse=True)
        
        # Keep top 20%
        elite_size = max(2, self.population_size // 5)
        new_population = self.population[:elite_size]
        
        # Generate offspring
        while len(new_population) < self.population_size:
            # Tournament selection
            parent = self.tournament_select()
            
            # Mutate
            offspring = parent.mutate()
            new_population.append(offspring)
        
        self.population = new_population
        self.generation += 1
    
    def tournament_select(self, tournament_size=3):
        """Select parent via tournament"""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda a: a.fitness)
    
    def get_best_architecture(self):
        """Get best architecture found"""
        return self.best_architecture
    
    def get_stats(self):
        """Get evolution statistics"""
        avg_fitness = np.mean([a.fitness for a in self.population])
        avg_complexity = np.mean([a.complexity for a in self.population])
        avg_layers = np.mean([a.num_layers for a in self.population])
        
        return {
            'generation': self.generation,
            'best_fitness': self.best_fitness,
            'best_accuracy': self.best_architecture.accuracy if self.best_architecture else 0,
            'avg_fitness': avg_fitness,
            'avg_complexity': avg_complexity,
            'avg_layers': avg_layers
        }
