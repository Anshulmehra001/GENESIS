#!/usr/bin/env python3
"""
Start EvolvAI Web Service
"""

import sys
import os

# Change to web directory
os.chdir(os.path.join(os.path.dirname(__file__), 'web'))

# Run Flask app
from app import app

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
