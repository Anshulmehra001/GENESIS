"""
Phase 4.5: Recursive Self-Improvement System
EXPERIMENTAL: Allows organisms to modify their own decision-making code
WARNING: This is potentially dangerous and disabled by default
"""

import random
import copy
from collections import deque

class CodeModification:
    """A proposed modification to organism's code"""
    def __init__(self, mod_id, target, change_type, parameters):
        self.id = mod_id
        self.target = target  # What to modify (e.g., 'decision_weights')
        self.change_type = change_type  # 'adjust', 'add', 'remove'
        self.parameters = parameters  # Modification details
        self.tested = False
        self.performance_before = 0.0
        self.performance_after = 0.0
        self.approved = False
        self.timestamp = 0
    
    def get_improvement(self):
        """Calculate performance improvement"""
        if not self.tested:
            return 0.0
        return self.performance_after - self.performance_before

class SafetySandbox:
    """Safe environment for testing modifications"""
    def __init__(self):
        self.test_history = deque(maxlen=100)
        self.failed_modifications = []
        self.dangerous_patterns = set()
    
    def is_safe(self, modification):
        """Check if modification is safe to test"""
        # Check against known dangerous patterns
        if modification.change_type in self.dangerous_patterns:
            return False
        
        # Don't allow too many modifications at once
        recent_mods = [m for m in self.test_history if m.timestamp > len(self.test_history) - 10]
        if len(recent_mods) > 5:
            return False
        
        return True
    
    def test_modification(self, organism, modification):
        """Test modification in sandbox"""
        # Create backup
        backup = self._create_backup(organism)
        
        try:
            # Apply modification
            self._apply_modification(organism, modification)
            
            # Simulate for a few steps
            performance = self._measure_performance(organism)
            
            modification.performance_after = performance
            modification.tested = True
            
            # Rollback
            self._restore_backup(organism, backup)
            
            return True
        
        except Exception as e:
            # Modification caused error - dangerous!
            self.dangerous_patterns.add(modification.change_type)
            self.failed_modifications.append(modification)
            
            # Rollback
            self._restore_backup(organism, backup)
            
            return False
    
    def _create_backup(self, organism):
        """Create backup of organism state"""
        return {
            'genome': copy.deepcopy(organism.genome),
            'energy': organism.energy,
            'x': organism.x,
            'y': organism.y
        }
    
    def _restore_backup(self, organism, backup):
        """Restore organism from backup"""
        organism.genome = backup['genome']
        organism.energy = backup['energy']
        organism.x = backup['x']
        organism.y = backup['y']
    
    def _apply_modification(self, organism, modification):
        """Apply modification to organism"""
        if modification.target == 'decision_weights':
            # Modify decision-making weights
            if 'move_probability' in organism.genome:
                organism.genome['move_probability'] *= modification.parameters.get('factor', 1.0)
                organism.genome['move_probability'] = max(0.0, min(1.0, organism.genome['move_probability']))
    
    def _measure_performance(self, organism):
        """Measure organism performance"""
        # Simple metric: energy level
        return organism.energy

class SelfModificationSystem:
    """Recursive self-improvement capabilities"""
    
    def __init__(self, organism):
        self.organism = organism
        
        # Safety
        self.sandbox = SafetySandbox()
        self.modifications_this_lifetime = 0
        self.max_modifications = 5
        
        # Modification history
        self.proposed_modifications = []
        self.applied_modifications = []
        self.rejected_modifications = []
        
        # Performance tracking
        self.performance_history = deque(maxlen=50)
        self.baseline_performance = 0.0
        
        # Meta-learning
        self.learning_strategies = {}
        self.strategy_performance = {}
    
    def can_self_modify(self):
        """Check if self-modification is allowed"""
        from config import ENABLE_SELF_MODIFICATION, MAX_MODIFICATIONS_PER_LIFETIME
        
        if not ENABLE_SELF_MODIFICATION:
            return False
        
        if self.modifications_this_lifetime >= MAX_MODIFICATIONS_PER_LIFETIME:
            return False
        
        return True
    
    def propose_modification(self):
        """Propose a modification to self"""
        if not self.can_self_modify():
            return None
        
        # Generate random modification
        mod_id = len(self.proposed_modifications)
        
        modification = CodeModification(
            mod_id=mod_id,
            target='decision_weights',
            change_type='adjust',
            parameters={'factor': random.uniform(0.8, 1.2)}
        )
        
        self.proposed_modifications.append(modification)
        return modification
    
    def test_modification(self, modification):
        """Test modification in sandbox"""
        from config import SELF_MOD_SAFETY_CHECKS
        
        if SELF_MOD_SAFETY_CHECKS:
            if not self.sandbox.is_safe(modification):
                self.rejected_modifications.append(modification)
                return False
        
        # Measure current performance
        modification.performance_before = self._current_performance()
        
        # Test in sandbox
        success = self.sandbox.test_modification(self.organism, modification)
        
        if not success:
            self.rejected_modifications.append(modification)
            return False
        
        # Check if improvement
        improvement = modification.get_improvement()
        
        if improvement > 0:
            modification.approved = True
            return True
        else:
            self.rejected_modifications.append(modification)
            return False
    
    def apply_modification(self, modification):
        """Apply approved modification"""
        from config import SELF_MOD_ROLLBACK
        
        if not modification.approved:
            return False
        
        # Create rollback point
        if SELF_MOD_ROLLBACK:
            self.rollback_point = self.sandbox._create_backup(self.organism)
        
        # Apply modification
        self.sandbox._apply_modification(self.organism, modification)
        
        self.applied_modifications.append(modification)
        self.modifications_this_lifetime += 1
        
        return True
    
    def rollback_last_modification(self):
        """Undo last modification"""
        if not self.applied_modifications:
            return False
        
        if hasattr(self, 'rollback_point'):
            self.sandbox._restore_backup(self.organism, self.rollback_point)
            
            last_mod = self.applied_modifications.pop()
            self.rejected_modifications.append(last_mod)
            
            return True
        
        return False
    
    def _current_performance(self):
        """Measure current performance"""
        if len(self.performance_history) == 0:
            return self.organism.energy
        
        return sum(self.performance_history) / len(self.performance_history)
    
    def record_performance(self, performance):
        """Record performance metric"""
        self.performance_history.append(performance)
    
    def meta_learn(self):
        """Learn how to learn better"""
        # Analyze which modifications worked
        if len(self.applied_modifications) > 3:
            successful = [m for m in self.applied_modifications if m.get_improvement() > 0]
            
            if successful:
                # Learn pattern of successful modifications
                avg_factor = sum([m.parameters.get('factor', 1.0) for m in successful]) / len(successful)
                
                self.learning_strategies['preferred_factor'] = avg_factor
    
    def get_stats(self):
        """Get self-modification statistics"""
        return {
            'modifications_proposed': len(self.proposed_modifications),
            'modifications_applied': len(self.applied_modifications),
            'modifications_rejected': len(self.rejected_modifications),
            'modifications_this_lifetime': self.modifications_this_lifetime,
            'avg_improvement': sum([m.get_improvement() for m in self.applied_modifications]) / len(self.applied_modifications) if self.applied_modifications else 0.0
        }
