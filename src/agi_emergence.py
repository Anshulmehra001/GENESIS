"""
Phase 5: AGI Emergence System
Implements general problem solving, autonomous goals, consciousness indicators, ethics
"""

import random
import math
from collections import defaultdict, deque
import numpy as np

class Problem:
    """A problem to solve"""
    def __init__(self, problem_id, domain, difficulty, description):
        self.id = problem_id
        self.domain = domain  # 'spatial', 'social', 'resource', 'abstract'
        self.difficulty = difficulty  # 0.0 to 1.0
        self.description = description
        self.solution = None
        self.solved_by = []
    
    def check_solution(self, solution):
        """Check if solution is correct"""
        # Simplified - in real system would be domain-specific
        return solution == self.solution

class Goal:
    """An autonomous goal"""
    def __init__(self, goal_id, description, priority=0.5):
        self.id = goal_id
        self.description = description
        self.priority = priority
        self.sub_goals = []
        self.parent_goal = None
        self.progress = 0.0
        self.completed = False
        self.intrinsic = True  # Not programmed
    
    def add_sub_goal(self, sub_goal):
        """Decompose into sub-goals"""
        sub_goal.parent_goal = self
        self.sub_goals.append(sub_goal)
    
    def update_progress(self):
        """Calculate progress based on sub-goals"""
        if not self.sub_goals:
            return self.progress
        
        completed_sub_goals = sum(1 for g in self.sub_goals if g.completed)
        self.progress = completed_sub_goals / len(self.sub_goals)
        
        if self.progress >= 1.0:
            self.completed = True
        
        return self.progress

class ConsciousnessMetrics:
    """Measure consciousness indicators"""
    def __init__(self):
        self.phi = 0.0  # Integrated Information Theory measure
        self.global_workspace_activity = 0.0
        self.attention_focus = None
        self.reportable_states = []
        self.qualia_indicators = {}
    
    def calculate_phi(self, organism):
        """Calculate integrated information (simplified)"""
        # Real IIT calculation is extremely complex
        # This is a simplified proxy
        
        if not hasattr(organism, 'reasoning'):
            return 0.0
        
        # Measure information integration across cognitive systems
        systems = 0
        if hasattr(organism, 'reasoning'):
            systems += 1
        if hasattr(organism, 'language'):
            systems += 1
        if hasattr(organism, 'self_awareness'):
            systems += 1
        if hasattr(organism, 'creativity'):
            systems += 1
        
        # More integrated systems = higher phi
        self.phi = systems / 4.0
        
        return self.phi
    
    def update_global_workspace(self, information):
        """Update global workspace (conscious access)"""
        # Information that reaches global workspace is "conscious"
        self.global_workspace_activity = len(information) / 100.0
        
        # Broadcast to all systems
        self.reportable_states.append(information)
        if len(self.reportable_states) > 10:
            self.reportable_states.pop(0)
    
    def direct_attention(self, focus):
        """Attention mechanism"""
        self.attention_focus = focus
    
    def report_internal_state(self):
        """Introspection - describe internal state"""
        if not self.reportable_states:
            return None
        
        return self.reportable_states[-1]
    
    def detect_qualia(self, experience_type):
        """Detect subjective experience markers"""
        # This is the "hard problem" - we can only detect correlates
        if experience_type not in self.qualia_indicators:
            self.qualia_indicators[experience_type] = 0.0
        
        self.qualia_indicators[experience_type] += 0.1

class EthicalSystem:
    """Ethical reasoning and behavior"""
    def __init__(self):
        self.fairness_norm = 0.5
        self.cooperation_norm = 0.5
        self.reputation = {}  # organism_id -> reputation score
        self.moral_emotions = {
            'guilt': 0.0,
            'empathy': 0.0,
            'compassion': 0.0
        }
        self.ethical_principles = []
    
    def evaluate_fairness(self, action, context):
        """Is action fair?"""
        # Simple fairness: equal treatment
        if 'distribution' in context:
            distribution = context['distribution']
            # Check if distribution is equal
            if len(set(distribution)) == 1:
                return 1.0  # Perfectly fair
            else:
                variance = np.var(distribution)
                return 1.0 / (1.0 + variance)
        
        return 0.5
    
    def should_cooperate(self, other_organism):
        """Decide whether to cooperate"""
        # Check reputation
        other_id = id(other_organism)
        reputation = self.reputation.get(other_id, 0.5)
        
        # Cooperate with high-reputation organisms
        return reputation > 0.6
    
    def punish_defector(self, defector):
        """Punish organism that defected"""
        defector_id = id(defector)
        
        # Lower reputation
        if defector_id not in self.reputation:
            self.reputation[defector_id] = 0.5
        
        self.reputation[defector_id] -= 0.1
        self.reputation[defector_id] = max(0.0, self.reputation[defector_id])
    
    def feel_guilt(self, action, harm_caused):
        """Experience guilt for harmful action"""
        self.moral_emotions['guilt'] += harm_caused * 0.1
        self.moral_emotions['guilt'] = min(1.0, self.moral_emotions['guilt'])
    
    def feel_empathy(self, other_organism, other_state):
        """Experience empathy for another's state"""
        if other_state == 'suffering':
            self.moral_emotions['empathy'] += 0.1
            self.moral_emotions['compassion'] += 0.1
    
    def justify_decision(self, action, context):
        """Provide ethical justification"""
        justification = {
            'action': action,
            'principle': 'unknown',
            'reasoning': ''
        }
        
        # Check which principle applies
        if self.fairness_norm > 0.7:
            justification['principle'] = 'fairness'
            justification['reasoning'] = 'Action promotes equal treatment'
        elif self.cooperation_norm > 0.7:
            justification['principle'] = 'cooperation'
            justification['reasoning'] = 'Action benefits group'
        
        return justification

class GeneralIntelligence:
    """AGI capabilities"""
    
    def __init__(self, organism):
        self.organism = organism
        
        # General problem solving
        self.problems_solved = {}  # domain -> count
        self.problem_history = deque(maxlen=100)
        self.transfer_learning_enabled = True
        
        # Autonomous goals
        self.goals = []
        self.goal_count = 0
        self.current_goal = None
        
        # Consciousness
        self.consciousness = ConsciousnessMetrics()
        
        # Ethics
        self.ethics = EthicalSystem()
        
        # Novelty search
        self.behavior_archive = []
        self.novelty_threshold = 0.5
        
        # Complexity tracking
        self.complexity_history = deque(maxlen=100)
        
        # Performance across domains
        self.domain_performance = defaultdict(list)
    
    def solve_problem(self, problem):
        """Attempt to solve a problem"""
        # Try to transfer knowledge from other domains
        if self.transfer_learning_enabled:
            similar_problems = self._find_similar_problems(problem)
            
            if similar_problems:
                # Apply solution from similar problem
                solution = self._transfer_solution(similar_problems[0], problem)
                
                if problem.check_solution(solution):
                    # Success!
                    self._record_success(problem)
                    return solution
        
        # Try zero-shot reasoning
        solution = self._reason_from_first_principles(problem)
        
        if problem.check_solution(solution):
            self._record_success(problem)
            return solution
        
        return None
    
    def _find_similar_problems(self, problem):
        """Find similar problems solved before"""
        similar = []
        
        for past_problem in self.problem_history:
            if past_problem.domain == problem.domain:
                similar.append(past_problem)
        
        return similar
    
    def _transfer_solution(self, source_problem, target_problem):
        """Transfer solution across problems"""
        # Simplified transfer
        return source_problem.solution
    
    def _reason_from_first_principles(self, problem):
        """Solve novel problem through reasoning"""
        # Use abstract reasoning if available
        if hasattr(self.organism, 'reasoning'):
            # Try to find analogy
            analogy = self.organism.reasoning.find_analogy(problem)
            if analogy:
                return analogy
        
        # Random guess (simplified)
        return f"solution_{random.randint(0, 100)}"
    
    def _record_success(self, problem):
        """Record successful problem solving"""
        self.problems_solved[problem.domain] = self.problems_solved.get(problem.domain, 0) + 1
        self.problem_history.append(problem)
        self.domain_performance[problem.domain].append(1.0)
    
    def form_goal(self, description, priority=0.5):
        """Create autonomous goal"""
        goal = Goal(self.goal_count, description, priority)
        self.goal_count += 1
        self.goals.append(goal)
        
        # Set as current goal if higher priority
        if not self.current_goal or goal.priority > self.current_goal.priority:
            self.current_goal = goal
        
        return goal
    
    def decompose_goal(self, goal, sub_goals_descriptions):
        """Break goal into sub-goals"""
        for desc in sub_goals_descriptions:
            sub_goal = Goal(self.goal_count, desc, goal.priority * 0.8)
            self.goal_count += 1
            goal.add_sub_goal(sub_goal)
    
    def pursue_goal(self):
        """Work toward current goal"""
        if not self.current_goal:
            # Form intrinsic goal
            self.current_goal = self.form_goal('explore_environment', 0.6)
        
        # Update progress
        self.current_goal.update_progress()
        
        # If completed, choose next goal
        if self.current_goal.completed:
            self.current_goal = self._select_next_goal()
        
        return self.current_goal
    
    def _select_next_goal(self):
        """Choose next goal to pursue"""
        incomplete_goals = [g for g in self.goals if not g.completed]
        
        if not incomplete_goals:
            # Form new goal
            return self.form_goal('master_new_skill', 0.5)
        
        # Choose highest priority
        return max(incomplete_goals, key=lambda g: g.priority)
    
    def measure_consciousness(self):
        """Calculate consciousness indicators"""
        phi = self.consciousness.calculate_phi(self.organism)
        
        # Update global workspace
        current_state = {
            'energy': self.organism.energy,
            'age': self.organism.age,
            'goal': self.current_goal.description if self.current_goal else None
        }
        self.consciousness.update_global_workspace(current_state)
        
        return phi
    
    def introspect(self):
        """Report internal state"""
        return self.consciousness.report_internal_state()
    
    def make_ethical_decision(self, action, context):
        """Evaluate action ethically"""
        fairness = self.ethics.evaluate_fairness(action, context)
        
        # Decide based on ethical norms
        if fairness < 0.3:
            # Unfair action - feel guilt
            self.ethics.feel_guilt(action, 1.0 - fairness)
            return False  # Don't do it
        
        return True  # Ethically acceptable
    
    def calculate_novelty(self, behavior):
        """Calculate behavior novelty"""
        if not self.behavior_archive:
            return 1.0
        
        # Compare to archive
        min_distance = float('inf')
        for archived_behavior in self.behavior_archive:
            distance = self._behavior_distance(behavior, archived_behavior)
            min_distance = min(min_distance, distance)
        
        return min_distance
    
    def _behavior_distance(self, behavior1, behavior2):
        """Calculate distance between behaviors"""
        # Simplified - hash-based distance
        return abs(hash(str(behavior1)) - hash(str(behavior2))) / (2**32)
    
    def archive_behavior(self, behavior):
        """Add novel behavior to archive"""
        novelty = self.calculate_novelty(behavior)
        
        if novelty > self.novelty_threshold:
            self.behavior_archive.append(behavior)
            return True
        
        return False
    
    def measure_complexity(self):
        """Measure organism complexity"""
        complexity = 0.0
        
        # Count cognitive systems
        if hasattr(self.organism, 'reasoning'):
            complexity += 1.0
        if hasattr(self.organism, 'language'):
            complexity += 1.0
        if hasattr(self.organism, 'self_awareness'):
            complexity += 1.0
        if hasattr(self.organism, 'creativity'):
            complexity += 1.0
        
        # Add genome complexity
        if hasattr(self.organism, 'genome'):
            complexity += len(self.organism.genome) / 10.0
        
        self.complexity_history.append(complexity)
        
        return complexity
    
    def is_complexity_increasing(self):
        """Check if complexity is increasing over time"""
        if len(self.complexity_history) < 10:
            return False
        
        recent = list(self.complexity_history)[-10:]
        older = list(self.complexity_history)[-20:-10] if len(self.complexity_history) >= 20 else recent
        
        return sum(recent) / len(recent) > sum(older) / len(older)
    
    def calculate_general_intelligence(self):
        """Measure general intelligence across domains"""
        if not self.domain_performance:
            return 0.0
        
        # Average performance across all domains
        all_performances = []
        for domain_perfs in self.domain_performance.values():
            all_performances.extend(domain_perfs)
        
        if not all_performances:
            return 0.0
        
        return sum(all_performances) / len(all_performances)
    
    def get_stats(self):
        """Get AGI statistics"""
        return {
            'problems_solved': sum(self.problems_solved.values()),
            'domains_mastered': len(self.domain_performance),
            'active_goals': len([g for g in self.goals if not g.completed]),
            'consciousness_phi': self.consciousness.phi,
            'general_intelligence': self.calculate_general_intelligence(),
            'complexity': self.measure_complexity(),
            'complexity_increasing': self.is_complexity_increasing(),
            'novel_behaviors': len(self.behavior_archive),
            'ethical_decisions': len(self.ethics.reputation)
        }
