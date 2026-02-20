"""
EvolvAI Web Service
Simple web interface for Neural Architecture Search
"""

from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import json
import threading
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from neural_architecture_search import NASEvolution
import numpy as np

app = Flask(__name__)

# Store active jobs
jobs = {}
job_counter = 0

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/evolve', methods=['POST'])
def evolve():
    """Start evolution job"""
    global job_counter
    
    # Get parameters
    data = request.json
    problem_type = data.get('problem_type', 'classification')
    generations = int(data.get('generations', 50))
    
    # Create job
    job_id = job_counter
    job_counter += 1
    
    jobs[job_id] = {
        'status': 'running',
        'progress': 0,
        'best_accuracy': 0,
        'result': None
    }
    
    # Start evolution in background
    thread = threading.Thread(
        target=run_evolution,
        args=(job_id, problem_type, generations)
    )
    thread.start()
    
    return jsonify({'job_id': job_id})

@app.route('/api/status/<int:job_id>')
def status(job_id):
    """Check job status"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/api/result/<int:job_id>')
def result(job_id):
    """Get job result"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    if job['status'] != 'complete':
        return jsonify({'error': 'Job not complete'}), 400
    
    return jsonify(job['result'])

def run_evolution(job_id, problem_type, generations):
    """Run evolution in background"""
    try:
        # Create sample dataset
        if problem_type == 'classification':
            # Simple XOR problem
            X_train = np.random.randn(200, 2)
            y_train = ((X_train[:, 0] > 0) ^ (X_train[:, 1] > 0)).astype(int)
            X_test = np.random.randn(100, 2)
            y_test = ((X_test[:, 0] > 0) ^ (X_test[:, 1] > 0)).astype(int)
            
            input_size = 2
            output_size = 2
        else:
            # Default to simple problem
            X_train = np.random.randn(200, 4)
            y_train = (X_train[:, 0] + X_train[:, 1] > 0).astype(int)
            X_test = np.random.randn(100, 4)
            y_test = (X_test[:, 0] + X_test[:, 1] > 0).astype(int)
            
            input_size = 4
            output_size = 2
        
        # Initialize NAS
        nas = NASEvolution(input_size, output_size, population_size=20)
        
        # Evolution loop
        for gen in range(generations):
            # Evaluate
            nas.evaluate_population(X_train, y_train, X_test, y_test)
            
            # Update progress
            stats = nas.get_stats()
            jobs[job_id]['progress'] = int((gen + 1) / generations * 100)
            jobs[job_id]['best_accuracy'] = float(stats['best_accuracy'])
            
            # Evolve
            nas.evolve_generation()
            
            time.sleep(0.1)  # Simulate work
        
        # Get best architecture
        best = nas.get_best_architecture()
        
        # Store result
        jobs[job_id]['status'] = 'complete'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['result'] = {
            'accuracy': float(best.accuracy),
            'layers': best.num_layers,
            'layer_sizes': best.layer_sizes,
            'activations': best.activations,
            'complexity': best.complexity,
            'architecture': best.to_dict()
        }
        
    except Exception as e:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                    EvolvAI Web Service                    ║
    ║                                                           ║
    ║         Evolve AI models through your browser             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🌐 Starting web server...
    📍 Open: http://localhost:5000
    """)
    
    app.run(debug=True, port=5000)
