"""
Phase 4: Abstract Reasoning System
Implements pattern recognition, categorization, analogy, causal reasoning
"""

import random
import numpy as np
from collections import defaultdict, deque

class Pattern:
    """Represents a recognized pattern"""
    def __init__(self, pattern_type, features, frequency=1):
        self.type = pattern_type  # 'sequence', 'spatial', 'causal'
        self.features = features  # Pattern characteristics
        self.frequency = frequency  # How often seen
        self.predictions = []  # What usually follows
        self.confidence = 0.0
    
    def update(self, outcome):
        """Update pattern based on new observation"""
        self.frequency += 1
        self.predictions.append(outcome)
        # Calculate confidence based on consistency
        if len(self.predictions) > 3:
            unique_outcomes = len(set(self.predictions[-10:]))
            self.confidence = 1.0 - (unique_outcomes / 10.0)

class Category:
    """Represents a learned category"""
    def __init__(self, name, prototype):
        self.name = name
        self.prototype = prototype  # Central example
        self.members = []  # Things in this category
        self.parent = None  # Hierarchical structure
        self.children = []
    
    def similarity(self, features):
        """Calculate similarity to prototype"""
        if not self.prototype:
            return 0.0
        # Simple feature overlap
        common = set(self.prototype.keys()) & set(features.keys())
        if not common:
            return 0.0
        matches = sum(1 for k in common if self.prototype[k] == features[k])
        return matches / len(common)

class CausalModel:
    """Represents cause-effect relationships"""
    def __init__(self):
        self.causes = defaultdict(list)  # action -> outcomes
        self.effects = defaultdict(list)  # outcome -> causes
        self.strengths = {}  # (cause, effect) -> strength
    
    def add_observation(self, cause, effect):
        """Learn from observation"""
        self.causes[cause].append(effect)
        self.effects[effect].append(cause)
        
        key = (cause, effect)
        if key not in self.strengths:
            self.strengths[key] = 0.0
        
        # Update causal strength
        total = len(self.causes[cause])
        effect_count = self.causes[cause].count(effect)
        self.strengths[key] = effect_count / total
    
    def predict(self, cause):
        """Predict most likely effect"""
        if cause not in self.causes:
            return None
        
        effects = self.causes[cause]
        if not effects:
            return None
        
        # Return most common effect
        return max(set(effects), key=effects.count)
    
    def plan_intervention(self, desired_effect):
        """Find action that causes desired effect"""
        if desired_effect not in self.effects:
            return None
        
        # Find strongest cause
        best_cause = None
        best_strength = 0.0
        
        for cause in self.effects[desired_effect]:
            strength = self.strengths.get((cause, desired_effect), 0.0)
            if strength > best_strength:
                best_strength = strength
                best_cause = cause
        
        return best_cause if best_strength > 0.3 else None

class AbstractReasoning:
    """Abstract reasoning capabilities for organisms"""
    
    def __init__(self, organism):
        self.organism = organism
        
        # Pattern recognition
        self.patterns = []
        self.pattern_memory = deque(maxlen=50)  # Recent observations
        
        # Categorization
        self.categories = {}
        self.category_count = 0
        
        # Causal reasoning
        self.causal_model = CausalModel()
        self.last_action = None
        self.last_state = None
        
        # Analogies
        self.analogies = []  # (domain1, domain2, mapping)
        
        # Counterfactuals
        self.counterfactuals = []  # "what if" scenarios
        self.regrets = []  # Missed opportunities
    
    def observe(self, observation):
        """Process new observation"""
        self.pattern_memory.append(observation)
        
        # Try to recognize patterns
        if len(self.pattern_memory) >= 3:
            self._recognize_patterns()
        
        # Update causal model
        if self.last_action and self.last_state:
            outcome = self._extract_outcome(observation)
            self.causal_model.add_observation(self.last_action, outcome)
        
        # Try to categorize
        self._categorize(observation)
    
    def _recognize_patterns(self):
        """Identify recurring patterns"""
        recent = list(self.pattern_memory)[-10:]
        
        # Look for sequences
        if len(recent) >= 3:
            # Check if last 3 observations repeat
            seq = tuple(recent[-3:])
            
            # See if this sequence appeared before
            for i in range(len(recent) - 6):
                if tuple(recent[i:i+3]) == seq:
                    # Found repeating pattern!
                    pattern = Pattern('sequence', seq)
                    
                    # What came next last time?
                    if i + 3 < len(recent):
                        pattern.predictions.append(recent[i+3])
                    
                    self.patterns.append(pattern)
                    break
    
    def predict_next(self):
        """Predict what will happen next"""
        if not self.patterns:
            return None
        
        # Find most confident pattern
        best_pattern = max(self.patterns, key=lambda p: p.confidence)
        
        if best_pattern.confidence > 0.5 and best_pattern.predictions:
            return best_pattern.predictions[-1]
        
        return None
    
    def _categorize(self, observation):
        """Assign observation to category"""
        features = self._extract_features(observation)
        
        # Try existing categories
        best_category = None
        best_similarity = 0.0
        
        for category in self.categories.values():
            sim = category.similarity(features)
            if sim > best_similarity:
                best_similarity = sim
                best_category = category
        
        # If similar enough, add to category
        if best_similarity > 0.6:
            best_category.members.append(observation)
        # Otherwise, create new category
        elif len(self.categories) < 20:  # Limit categories
            name = f"category_{self.category_count}"
            self.category_count += 1
            new_cat = Category(name, features)
            new_cat.members.append(observation)
            self.categories[name] = new_cat
    
    def find_analogy(self, problem):
        """Find analogous situation from past"""
        problem_features = self._extract_features(problem)
        
        # Look through categories for similar structure
        for category in self.categories.values():
            if len(category.members) > 1:
                # Check if problem structure matches category
                sim = category.similarity(problem_features)
                if sim > 0.4:
                    # Found analogy! Return similar past situation
                    return random.choice(category.members)
        
        return None
    
    def reason_causally(self, goal):
        """Use causal model to plan action"""
        action = self.causal_model.plan_intervention(goal)
        return action
    
    def counterfactual(self, past_action, alternative_action):
        """Imagine 'what if I had done X instead?'"""
        # Predict what would have happened
        actual_outcome = self.causal_model.predict(past_action)
        alternative_outcome = self.causal_model.predict(alternative_action)
        
        if alternative_outcome and actual_outcome:
            # Compare outcomes
            cf = {
                'actual_action': past_action,
                'actual_outcome': actual_outcome,
                'alternative_action': alternative_action,
                'alternative_outcome': alternative_outcome
            }
            self.counterfactuals.append(cf)
            
            # Feel regret if alternative was better
            if self._is_better(alternative_outcome, actual_outcome):
                self.regrets.append(cf)
            
            return cf
        
        return None
    
    def _extract_features(self, observation):
        """Extract features from observation"""
        if isinstance(observation, dict):
            return observation
        
        # Simple feature extraction
        return {
            'type': type(observation).__name__,
            'value': str(observation)[:20]
        }
    
    def _extract_outcome(self, observation):
        """Extract outcome from observation"""
        if isinstance(observation, dict) and 'outcome' in observation:
            return observation['outcome']
        return 'unknown'
    
    def _is_better(self, outcome1, outcome2):
        """Compare outcomes"""
        # Simple heuristic: more energy is better
        if isinstance(outcome1, dict) and isinstance(outcome2, dict):
            return outcome1.get('energy', 0) > outcome2.get('energy', 0)
        return False
    
    def record_action(self, action, state):
        """Record action for causal learning"""
        self.last_action = action
        self.last_state = state
    
    def get_stats(self):
        """Get reasoning statistics"""
        return {
            'patterns_recognized': len(self.patterns),
            'categories_formed': len(self.categories),
            'causal_links': len(self.causal_model.strengths),
            'analogies_found': len(self.analogies),
            'counterfactuals': len(self.counterfactuals),
            'regrets': len(self.regrets)
        }
