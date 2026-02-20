"""
Phase 4: Self-Awareness System
Implements self-recognition, self-modeling, theory of mind, metacognition
"""

import random
from collections import deque, defaultdict

class SelfModel:
    """Internal model of self"""
    def __init__(self, organism):
        self.organism = organism
        
        # Self-knowledge
        self.traits = {}  # Known traits about self
        self.capabilities = set()  # What I can do
        self.limitations = set()  # What I can't do
        
        # Self-history
        self.past_actions = deque(maxlen=100)
        self.past_outcomes = deque(maxlen=100)
        
        # Self-prediction
        self.predicted_actions = {}  # situation -> likely action
        self.prediction_accuracy = 0.0
    
    def update_trait(self, trait, value):
        """Learn about self"""
        self.traits[trait] = value
    
    def record_action(self, action, outcome):
        """Record what I did and what happened"""
        self.past_actions.append(action)
        self.past_outcomes.append(outcome)
        
        # Learn patterns in own behavior
        if len(self.past_actions) > 10:
            self._learn_self_patterns()
    
    def _learn_self_patterns(self):
        """Identify patterns in own behavior"""
        # Simple pattern: what do I usually do?
        action_counts = defaultdict(int)
        for action in list(self.past_actions)[-20:]:
            action_counts[action] += 1
        
        # Most common action
        if action_counts:
            most_common = max(action_counts, key=action_counts.get)
            self.traits['typical_action'] = most_common
    
    def predict_self(self, situation):
        """Predict what I would do"""
        # Check if I've been in similar situation
        if situation in self.predicted_actions:
            return self.predicted_actions[situation]
        
        # Use typical behavior
        if 'typical_action' in self.traits:
            return self.traits['typical_action']
        
        return None
    
    def verify_prediction(self, situation, actual_action):
        """Check if self-prediction was accurate"""
        predicted = self.predict_self(situation)
        
        if predicted == actual_action:
            self.prediction_accuracy += 0.1
        else:
            self.prediction_accuracy -= 0.05
        
        # Clamp
        self.prediction_accuracy = max(0.0, min(1.0, self.prediction_accuracy))
        
        # Update model
        self.predicted_actions[situation] = actual_action
    
    def get_self_knowledge(self):
        """Return what I know about myself"""
        return {
            'traits': self.traits,
            'capabilities': len(self.capabilities),
            'limitations': len(self.limitations),
            'prediction_accuracy': self.prediction_accuracy
        }

class OtherModel:
    """Model of another organism's mind"""
    def __init__(self, other_organism):
        self.other = other_organism
        
        # Observed traits
        self.observed_traits = {}
        self.observed_actions = deque(maxlen=50)
        
        # Predictions about other
        self.predicted_actions = {}
        self.prediction_accuracy = 0.0
        
        # Beliefs about other's beliefs
        self.their_beliefs = {}  # What I think they think
    
    def observe(self, action, context):
        """Observe other's behavior"""
        self.observed_actions.append((action, context))
        
        # Learn their patterns
        if len(self.observed_actions) > 5:
            self._infer_traits()
    
    def _infer_traits(self):
        """Infer traits from behavior"""
        recent = list(self.observed_actions)[-10:]
        
        # Count action types
        action_counts = defaultdict(int)
        for action, _ in recent:
            action_counts[action] += 1
        
        # Infer personality
        if action_counts.get('attack', 0) > 5:
            self.observed_traits['aggressive'] = True
        if action_counts.get('share', 0) > 5:
            self.observed_traits['cooperative'] = True
    
    def predict_other(self, situation):
        """Predict what other will do"""
        # Use observed patterns
        if situation in self.predicted_actions:
            return self.predicted_actions[situation]
        
        # Use inferred traits
        if self.observed_traits.get('aggressive'):
            return 'attack'
        if self.observed_traits.get('cooperative'):
            return 'cooperate'
        
        return None
    
    def verify_prediction(self, situation, actual_action):
        """Check prediction accuracy"""
        predicted = self.predict_other(situation)
        
        if predicted == actual_action:
            self.prediction_accuracy += 0.1
        else:
            self.prediction_accuracy -= 0.05
        
        self.prediction_accuracy = max(0.0, min(1.0, self.prediction_accuracy))
        
        # Update model
        self.predicted_actions[situation] = actual_action
    
    def model_their_belief(self, belief, value):
        """Model what other believes"""
        self.their_beliefs[belief] = value
    
    def can_deceive(self):
        """Can I deceive them?"""
        # Deception requires theory of mind
        return len(self.their_beliefs) > 0

class Metacognition:
    """Thinking about thinking"""
    def __init__(self, organism):
        self.organism = organism
        
        # Monitor own thoughts
        self.thought_history = deque(maxlen=50)
        self.current_thought = None
        
        # Cognitive control
        self.attention_focus = None
        self.cognitive_load = 0.0
        
        # Self-evaluation
        self.performance_history = deque(maxlen=20)
        self.self_assessment = 0.5  # How well am I doing?
    
    def think(self, thought):
        """Record a thought"""
        self.current_thought = thought
        self.thought_history.append(thought)
    
    def monitor(self):
        """Monitor own cognitive state"""
        # Check cognitive load
        self.cognitive_load = len(self.thought_history) / 50.0
        
        # Assess if thinking is productive
        if len(self.performance_history) > 5:
            recent_performance = list(self.performance_history)[-5:]
            self.self_assessment = sum(recent_performance) / len(recent_performance)
    
    def control_attention(self, focus):
        """Direct attention"""
        self.attention_focus = focus
    
    def evaluate_performance(self, outcome):
        """Evaluate how well I did"""
        # Simple: positive outcome = good performance
        performance = 1.0 if outcome == 'success' else 0.0
        self.performance_history.append(performance)
        
        self.monitor()
    
    def should_change_strategy(self):
        """Decide if current approach is working"""
        if len(self.performance_history) < 5:
            return False
        
        # If recent performance is poor, change strategy
        return self.self_assessment < 0.3
    
    def reflect(self):
        """Reflect on recent thoughts and actions"""
        if len(self.thought_history) < 10:
            return None
        
        # Analyze thought patterns
        recent_thoughts = list(self.thought_history)[-10:]
        
        # Are thoughts repetitive?
        unique_thoughts = len(set(recent_thoughts))
        repetitive = unique_thoughts < 5
        
        # Are thoughts productive?
        productive = self.self_assessment > 0.5
        
        return {
            'repetitive': repetitive,
            'productive': productive,
            'cognitive_load': self.cognitive_load,
            'self_assessment': self.self_assessment
        }

class SelfAwareness:
    """Self-awareness capabilities for organisms"""
    
    def __init__(self, organism):
        self.organism = organism
        
        # Self-recognition
        self.self_id = id(organism)
        self.recognizes_self = False
        
        # Self-model
        self.self_model = SelfModel(organism)
        
        # Models of others
        self.other_models = {}  # organism_id -> OtherModel
        
        # Metacognition
        self.metacognition = Metacognition(organism)
        
        # Self-reflection
        self.reflections = []
        self.last_reflection_time = 0
    
    def recognize_self(self, organism):
        """Check if organism is self"""
        is_self = id(organism) == self.self_id
        
        if is_self and not self.recognizes_self:
            # First time recognizing self!
            self.recognizes_self = True
        
        return is_self
    
    def update_self_model(self, action, outcome):
        """Learn about self from experience"""
        self.self_model.record_action(action, outcome)
    
    def predict_self_action(self, situation):
        """Predict own behavior"""
        return self.self_model.predict_self(situation)
    
    def get_other_model(self, other_organism):
        """Get or create model of other"""
        other_id = id(other_organism)
        
        if other_id not in self.other_models:
            self.other_models[other_id] = OtherModel(other_organism)
        
        return self.other_models[other_id]
    
    def observe_other(self, other_organism, action, context):
        """Observe and model other's behavior"""
        model = self.get_other_model(other_organism)
        model.observe(action, context)
    
    def predict_other_action(self, other_organism, situation):
        """Predict what other will do"""
        model = self.get_other_model(other_organism)
        return model.predict_other(situation)
    
    def can_deceive(self, other_organism):
        """Check if can deceive other"""
        model = self.get_other_model(other_organism)
        return model.can_deceive()
    
    def think(self, thought):
        """Have a thought"""
        self.metacognition.think(thought)
    
    def reflect(self, current_time):
        """Self-reflection"""
        # Reflect periodically
        if current_time - self.last_reflection_time > 100:
            reflection = self.metacognition.reflect()
            
            if reflection:
                self.reflections.append(reflection)
                
                # Act on reflection
                if reflection['repetitive'] and not reflection['productive']:
                    # Stuck in unproductive loop
                    return 'change_strategy'
            
            self.last_reflection_time = current_time
        
        return None
    
    def evaluate_self(self, outcome):
        """Evaluate own performance"""
        self.metacognition.evaluate_performance(outcome)
    
    def get_self_knowledge(self):
        """What do I know about myself?"""
        return self.self_model.get_self_knowledge()
    
    def get_stats(self):
        """Get self-awareness statistics"""
        return {
            'recognizes_self': self.recognizes_self,
            'self_prediction_accuracy': self.self_model.prediction_accuracy,
            'other_models': len(self.other_models),
            'reflections': len(self.reflections),
            'cognitive_load': self.metacognition.cognitive_load,
            'self_assessment': self.metacognition.self_assessment
        }
