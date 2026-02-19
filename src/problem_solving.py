"""
Problem Solving Challenges
Puzzles and challenges for organisms to solve
"""

import random

class Puzzle:
    """A puzzle environment"""
    
    def __init__(self, x, y, puzzle_type):
        self.x = x
        self.y = y
        self.type = puzzle_type  # 'maze', 'locked_resource', 'multi_step'
        self.solved = False
        self.reward = 500
        self.required_steps = []
        self.completed_steps = []
        
        if puzzle_type == 'maze':
            self.required_steps = ['north', 'east', 'south', 'east']
        elif puzzle_type == 'locked_resource':
            self.required_steps = ['find_key', 'use_key']
        elif puzzle_type == 'multi_step':
            self.required_steps = ['activate_a', 'activate_b', 'activate_c']
    
    def attempt_step(self, step):
        """Attempt a puzzle step"""
        if self.solved:
            return False
        
        if len(self.completed_steps) < len(self.required_steps):
            expected_step = self.required_steps[len(self.completed_steps)]
            if step == expected_step:
                self.completed_steps.append(step)
                if len(self.completed_steps) == len(self.required_steps):
                    self.solved = True
                return True
        return False
    
    def get_reward(self):
        """Get reward for solving puzzle"""
        if self.solved:
            reward = self.reward
            self.reward = 0
            return reward
        return 0


class ProblemSolver:
    """Mixin for organisms that can solve problems"""
    
    def __init__(self):
        self.attempted_solutions = []
        self.successful_solutions = []
        self.insights = []
    
    def try_solution(self, puzzle, solution):
        """Try a solution to a puzzle"""
        self.attempted_solutions.append((puzzle.type, solution))
        
        success = puzzle.attempt_step(solution)
        
        if success:
            self.successful_solutions.append((puzzle.type, solution))
            
            # Insight: recognize pattern
            if len(self.successful_solutions) > 3:
                self.gain_insight(puzzle.type)
        
        return success
    
    def gain_insight(self, puzzle_type):
        """Gain insight about puzzle type"""
        if puzzle_type not in self.insights:
            self.insights.append(puzzle_type)
    
    def has_insight(self, puzzle_type):
        """Check if has insight about puzzle type"""
        return puzzle_type in self.insights
    
    def plan_solution(self, puzzle):
        """Plan multi-step solution"""
        if self.has_insight(puzzle.type):
            # Use known solution
            return puzzle.required_steps.copy()
        else:
            # Trial and error
            return [random.choice(['north', 'south', 'east', 'west', 'find_key', 'use_key', 'activate_a', 'activate_b', 'activate_c'])]
