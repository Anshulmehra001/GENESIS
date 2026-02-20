"""
Save and Load System
Allows simulation to persist across sessions
"""

import pickle
import json
import os
from datetime import datetime

class SimulationSaver:
    """Save and load simulation state"""
    
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save(self, universe, filename=None):
        """Save entire universe state"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"genesis_save_{timestamp}.pkl"
        
        filepath = os.path.join(self.save_dir, filename)
        
        # Save universe state
        save_data = {
            'tick': universe.tick,
            'energy_grid': universe.energy_grid,
            'organisms': universe.organisms,
            'stats': universe.stats,
            'signals': getattr(universe, 'signals', []),
            'structures': getattr(universe, 'structures', []),
            'puzzles': getattr(universe, 'puzzles', [])
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)
        
        # Also save metadata as JSON
        metadata = {
            'tick': universe.tick,
            'population': len(universe.organisms),
            'timestamp': datetime.now().isoformat(),
            'stats': {k: v for k, v in universe.stats.items() if isinstance(v, (int, float, str))}
        }
        
        meta_filepath = filepath.replace('.pkl', '_meta.json')
        with open(meta_filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Saved to: {filepath}")
        return filepath
    
    def load(self, filename):
        """Load universe state"""
        filepath = os.path.join(self.save_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ Save file not found: {filepath}")
            return None
        
        with open(filepath, 'rb') as f:
            save_data = pickle.load(f)
        
        print(f"✅ Loaded from: {filepath}")
        print(f"   Tick: {save_data['tick']}")
        print(f"   Population: {len(save_data['organisms'])}")
        
        return save_data
    
    def list_saves(self):
        """List all save files"""
        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.pkl'):
                filepath = os.path.join(self.save_dir, filename)
                meta_filepath = filepath.replace('.pkl', '_meta.json')
                
                if os.path.exists(meta_filepath):
                    with open(meta_filepath, 'r') as f:
                        metadata = json.load(f)
                    saves.append({
                        'filename': filename,
                        'metadata': metadata
                    })
        
        return sorted(saves, key=lambda x: x['metadata']['timestamp'], reverse=True)
    
    def autosave(self, universe, interval=1000):
        """Auto-save every N ticks"""
        if universe.tick % interval == 0:
            filename = f"autosave_tick_{universe.tick}.pkl"
            self.save(universe, filename)
            
            # Keep only last 5 autosaves
            self.cleanup_old_autosaves(keep=5)
    
    def cleanup_old_autosaves(self, keep=5):
        """Remove old autosaves, keep only recent ones"""
        autosaves = [f for f in os.listdir(self.save_dir) if f.startswith('autosave_')]
        autosaves.sort(reverse=True)
        
        for old_save in autosaves[keep:]:
            filepath = os.path.join(self.save_dir, old_save)
            os.remove(filepath)
            meta_filepath = filepath.replace('.pkl', '_meta.json')
            if os.path.exists(meta_filepath):
                os.remove(meta_filepath)

def restore_universe(save_data, universe):
    """Restore universe from save data"""
    universe.tick = save_data['tick']
    universe.energy_grid = save_data['energy_grid']
    universe.organisms = save_data['organisms']
    universe.stats = save_data['stats']
    
    if 'signals' in save_data:
        universe.signals = save_data['signals']
    if 'structures' in save_data:
        universe.structures = save_data['structures']
    if 'puzzles' in save_data:
        universe.puzzles = save_data['puzzles']
    
    return universe
