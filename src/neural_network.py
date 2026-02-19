"""
Neural Network Brain for Organisms
Simple feedforward neural network that evolves through mutation
"""

import numpy as np
import random
from config import *

class NeuralNetwork:
    """Simple neural network for organism decision-making"""
    
    def __init__(self, input_size=10, hidden_sizes=[8, 8], output_size=6):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        
        # Initialize weights randomly
        self.weights = []
        self.biases = []
        
        # Input to first hidden layer
        prev_size = input_size
        for hidden_size in hidden_sizes:
            self.weights.append(np.random.randn(prev_size, hidden_size) * 0.5)
            self.biases.append(np.zeros(hidden_size))
            prev_size = hidden_size
        
        # Last hidden to output
        self.weights.append(np.random.randn(prev_size, output_size) * 0.5)
        self.biases.append(np.zeros(output_size))
    
    def forward(self, inputs):
        """Forward pass through network"""
        activation = np.array(inputs)
        
        # Hidden layers with ReLU
        for i in range(len(self.weights) - 1):
            activation = np.maximum(0, np.dot(activation, self.weights[i]) + self.biases[i])
        
        # Output layer with sigmoid
        output = 1 / (1 + np.exp(-(np.dot(activation, self.weights[-1]) + self.biases[-1])))
        
        return output
    
    def mutate(self, mutation_rate=0.1, mutation_strength=0.2):
        """Mutate network weights"""
        for i in range(len(self.weights)):
            if random.random() < mutation_rate:
                # Mutate weights
                mask = np.random.random(self.weights[i].shape) < mutation_rate
                self.weights[i] += mask * np.random.randn(*self.weights[i].shape) * mutation_strength
                
                # Mutate biases
                mask = np.random.random(self.biases[i].shape) < mutation_rate
                self.biases[i] += mask * np.random.randn(*self.biases[i].shape) * mutation_strength
    
    def copy(self):
        """Create a copy of this network"""
        new_net = NeuralNetwork(self.input_size, self.hidden_sizes, self.output_size)
        new_net.weights = [w.copy() for w in self.weights]
        new_net.biases = [b.copy() for b in self.biases]
        return new_net
