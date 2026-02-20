"""
Phase 4: Creativity & Innovation System
Implements novel behavior generation, exploration, intrinsic motivation, play
"""

import random
import math
from collections import deque, defaultdict

class NovelBehavior:
    """A newly invented behavior"""
    def __init__(self, behavior_id, actions, context):
        self.id = behavior_id
        self.actions = actions  # Sequence of actions
        self.context = context  # When to use it
        self.success_count = 0
        self.failure_count = 0
        self.novelty_score = 1.0  # How novel is it?
        self.age = 0
    
    def evaluate(self, outcome):
        """Update based on outcome"""
        if outcome == 'success':
            self.success_count += 1
        else:
            self.failure_count += 1
        
        self.age += 1
        
        # Novelty decays over time
        self.novelty_score *= 0.99
    
    def get_fitness(self):
        """How good is this behavior?"""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.5  # Unknown
        return self.success_count / total

class CuriosityDrive:
    """Intrinsic motivation to explore"""
    def __init__(self):
        self.curiosity_level = 0.5
        self.explored_states = set()
        self.state_visit_counts = defaultdict(int)
        self.surprises = deque(maxlen=20)
    
    def get_curiosity(self, state):
        """How curious about this state?"""
        state_hash = hash(str(state))
        
        # More curious about less-visited states
        visit_count = self.state_visit_counts[state_hash]
        
        if visit_count == 0:
            return 1.0  # Maximum curiosity for new states
        
        # Curiosity decreases with familiarity
        return 1.0 / math.sqrt(visit_count + 1)
    
    def visit_state(self, state):
        """Record state visit"""
        state_hash = hash(str(state))
        self.state_visit_counts[state_hash] += 1
        self.explored_states.add(state_hash)
    
    def experience_surprise(self, expected, actual):
        """Record surprising outcome"""
        if expected != actual:
            surprise = abs(hash(expected) - hash(actual))
            self.surprises.append(surprise)
            
            # Surprise increases curiosity
            self.curiosity_level = min(1.0, self.curiosity_level + 0.1)
    
    def get_exploration_bonus(self, state):
        """Reward for exploring"""
        curiosity = self.get_curiosity(state)
        return curiosity * self.curiosity_level

class PlayBehavior:
    """Play without immediate benefit"""
    def __init__(self):
        self.play_sessions = []
        self.skills_practiced = defaultdict(int)
        self.play_energy = 0.0
    
    def should_play(self, energy_level, safety_level):
        """Decide if conditions are right for play"""
        # Play when safe and well-fed
        return energy_level > 0.7 and safety_level > 0.6
    
    def play(self, skill):
        """Practice skill through play"""
        self.skills_practiced[skill] += 1
        self.play_sessions.append({
            'skill': skill,
            'timestamp': len(self.play_sessions)
        })
    
    def get_skill_level(self, skill):
        """How much practiced?"""
        practice_count = self.skills_practiced[skill]
        # Skill improves with practice
        return min(1.0, practice_count / 100.0)

class Innovation:
    """Track and spread innovations"""
    def __init__(self):
        self.innovations = []  # List of NovelBehavior
        self.next_id = 0
        self.adoption_network = defaultdict(set)  # who learned from whom
    
    def create_innovation(self, actions, context):
        """Create new behavior"""
        innovation = NovelBehavior(self.next_id, actions, context)
        self.next_id += 1
        self.innovations.append(innovation)
        return innovation
    
    def adopt_innovation(self, innovation, adopter, source):
        """Organism adopts innovation from another"""
        self.adoption_network[innovation.id].add((adopter, source))
    
    def get_diffusion_rate(self, innovation):
        """How fast is innovation spreading?"""
        adopters = len(self.adoption_network[innovation.id])
        if innovation.age == 0:
            return 0.0
        return adopters / innovation.age

class CreativitySystem:
    """Creativity and innovation capabilities"""
    
    def __init__(self, organism):
        self.organism = organism
        
        # Novel behaviors
        self.novel_behaviors = []
        self.behavior_repertoire = set()  # Known behaviors
        
        # Exploration vs exploitation
        self.exploration_rate = 0.3  # How often to try new things
        self.exploitation_rate = 0.7  # How often to use known good behaviors
        
        # Curiosity
        self.curiosity = CuriosityDrive()
        
        # Intrinsic motivation
        self.mastery_goals = {}  # skill -> target level
        self.autonomy_level = 0.5  # How much control over own actions
        
        # Play
        self.play = PlayBehavior()
        
        # Innovation tracking
        self.innovations_created = 0
        self.innovations_adopted = 0
    
    def should_explore(self, state):
        """Decide whether to explore or exploit"""
        # Base exploration rate
        explore_prob = self.exploration_rate
        
        # Curiosity bonus
        curiosity_bonus = self.curiosity.get_curiosity(state)
        explore_prob += curiosity_bonus * 0.2
        
        # Random exploration
        return random.random() < explore_prob
    
    def generate_novel_behavior(self, context):
        """Create new behavior"""
        # Combine existing behaviors in new ways
        if len(self.behavior_repertoire) >= 2:
            # Recombination
            behaviors = random.sample(list(self.behavior_repertoire), 2)
            novel_actions = list(behaviors[0]) + list(behaviors[1])
        else:
            # Random variation
            novel_actions = [f"action_{random.randint(0, 10)}" 
                           for _ in range(random.randint(2, 5))]
        
        # Create novel behavior
        behavior = NovelBehavior(
            len(self.novel_behaviors),
            novel_actions,
            context
        )
        
        self.novel_behaviors.append(behavior)
        self.innovations_created += 1
        
        return behavior
    
    def evaluate_behavior(self, behavior, outcome):
        """Update behavior based on outcome"""
        behavior.evaluate(outcome)
        
        # If successful, add to repertoire
        if behavior.get_fitness() > 0.6:
            self.behavior_repertoire.add(tuple(behavior.actions))
    
    def learn_from_other(self, other_organism, behavior):
        """Social learning - copy innovation"""
        # Adopt behavior from other
        if hasattr(other_organism, 'creativity'):
            self.behavior_repertoire.add(tuple(behavior.actions))
            self.innovations_adopted += 1
            return True
        return False
    
    def set_mastery_goal(self, skill, target_level):
        """Set intrinsic goal to master skill"""
        self.mastery_goals[skill] = target_level
    
    def pursue_mastery(self):
        """Work toward mastery goals"""
        for skill, target in self.mastery_goals.items():
            current = self.play.get_skill_level(skill)
            
            if current < target:
                # Practice skill
                self.play.play(skill)
                return skill
        
        return None
    
    def should_play(self, energy, safety):
        """Decide if should engage in play"""
        return self.play.should_play(energy, safety)
    
    def engage_play(self):
        """Playful exploration"""
        # Choose random skill to practice
        skills = ['movement', 'sensing', 'communication', 'tool_use']
        skill = random.choice(skills)
        
        self.play.play(skill)
        
        # Play might lead to innovation
        if random.random() < 0.1:
            return self.generate_novel_behavior('play')
        
        return None
    
    def calculate_novelty(self, behavior):
        """How novel is this behavior?"""
        # Check similarity to existing behaviors
        if not self.behavior_repertoire:
            return 1.0
        
        # Simple novelty: not in repertoire
        if tuple(behavior.actions) not in self.behavior_repertoire:
            return 1.0
        
        return 0.0
    
    def get_most_novel_behaviors(self, n=5):
        """Get most novel behaviors"""
        sorted_behaviors = sorted(
            self.novel_behaviors,
            key=lambda b: b.novelty_score,
            reverse=True
        )
        return sorted_behaviors[:n]
    
    def get_best_behaviors(self, n=5):
        """Get most successful behaviors"""
        sorted_behaviors = sorted(
            self.novel_behaviors,
            key=lambda b: b.get_fitness(),
            reverse=True
        )
        return sorted_behaviors[:n]
    
    def update_exploration_rate(self, success_rate):
        """Adapt exploration based on success"""
        if success_rate < 0.3:
            # Not doing well, explore more
            self.exploration_rate = min(0.5, self.exploration_rate + 0.05)
        elif success_rate > 0.7:
            # Doing well, exploit more
            self.exploration_rate = max(0.1, self.exploration_rate - 0.05)
        
        self.exploitation_rate = 1.0 - self.exploration_rate
    
    def record_state_visit(self, state):
        """Record visiting state"""
        self.curiosity.visit_state(state)
    
    def record_surprise(self, expected, actual):
        """Record surprising outcome"""
        self.curiosity.experience_surprise(expected, actual)
    
    def get_stats(self):
        """Get creativity statistics"""
        return {
            'novel_behaviors': len(self.novel_behaviors),
            'behavior_repertoire': len(self.behavior_repertoire),
            'exploration_rate': self.exploration_rate,
            'curiosity_level': self.curiosity.curiosity_level,
            'states_explored': len(self.curiosity.explored_states),
            'innovations_created': self.innovations_created,
            'innovations_adopted': self.innovations_adopted,
            'play_sessions': len(self.play.play_sessions),
            'skills_practiced': len(self.play.skills_practiced)
        }
