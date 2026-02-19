"""
Extensions for Organism class
Additional methods for Phase 2 & 3 features
"""

def add_tool_methods(organism_class):
    """Add tool-related methods to Organism"""
    
    def create_tool(self, tool_type):
        """Create a tool"""
        from structures import Tool
        if self.energy >= 30:
            tool = Tool(tool_type)
            self.tools.append(tool)
            self.energy -= 30
            return tool
        return None
    
    def use_tool(self, tool_type):
        """Use a tool"""
        for tool in self.tools:
            if tool.type == tool_type and not tool.is_broken():
                return tool.use()
        return 1.0
    
    organism_class.create_tool = create_tool
    organism_class.use_tool = use_tool


def add_structure_methods(organism_class):
    """Add structure-related methods to Organism"""
    
    def build_structure(self, universe, structure_type):
        """Build a structure at current location"""
        from structures import Structure
        from config import STRUCTURE_BUILD_COST
        
        if self.energy >= STRUCTURE_BUILD_COST:
            structure = Structure(self.x, self.y, structure_type, self)
            self.built_structures.append(structure)
            universe.add_structure(structure)
            self.energy -= STRUCTURE_BUILD_COST
            return structure
        return None
    
    def use_structure(self, structure):
        """Use a structure"""
        benefit = structure.get_benefit(self)
        if 'energy' in benefit:
            energy_gained = benefit['energy']
            self.energy += energy_gained
            structure.stored_energy -= energy_gained
            return True
        return False
    
    organism_class.build_structure = build_structure
    organism_class.use_structure = use_structure


def add_problem_solving_methods(organism_class):
    """Add problem-solving methods to Organism"""
    
    def solve_puzzle(self, puzzle):
        """Attempt to solve a puzzle"""
        if hasattr(self, 'insights') and puzzle.type in self.insights:
            # Use known solution
            for step in puzzle.required_steps:
                if not puzzle.attempt_step(step):
                    break
        else:
            # Trial and error
            import random
            possible_steps = ['north', 'south', 'east', 'west', 'find_key', 'use_key', 
                            'activate_a', 'activate_b', 'activate_c']
            step = random.choice(possible_steps)
            success = puzzle.attempt_step(step)
            
            if success:
                self.successful_solutions.append((puzzle.type, step))
                if len(self.successful_solutions) > 3:
                    self.gain_insight(puzzle.type)
        
        if puzzle.solved:
            reward = puzzle.get_reward()
            self.energy += reward
            return True
        return False
    
    def gain_insight(self, puzzle_type):
        """Gain insight about puzzle type"""
        if puzzle_type not in self.insights:
            self.insights.append(puzzle_type)
    
    organism_class.solve_puzzle = solve_puzzle
    organism_class.gain_insight = gain_insight


def add_hierarchy_methods(organism_class):
    """Add social hierarchy methods to Organism"""
    
    def join_hierarchy(self, hierarchy):
        """Join a social hierarchy"""
        self.hierarchy = hierarchy
        hierarchy.add_member(self)
        self.role = hierarchy.get_role(self)
        self.rank = hierarchy.get_rank(self)
    
    def leave_hierarchy(self):
        """Leave social hierarchy"""
        if self.hierarchy:
            self.hierarchy.remove_member(self)
            self.hierarchy = None
            self.role = 'follower'
            self.rank = 999
    
    def challenge_rank(self, target):
        """Challenge another organism for rank"""
        from config import CHALLENGE_ENERGY_COST
        if self.hierarchy and self.energy >= CHALLENGE_ENERGY_COST:
            self.energy -= CHALLENGE_ENERGY_COST
            success = self.hierarchy.challenge(self, target)
            if success:
                self.role = self.hierarchy.get_role(self)
                self.rank = self.hierarchy.get_rank(self)
            return success
        return False
    
    organism_class.join_hierarchy = join_hierarchy
    organism_class.leave_hierarchy = leave_hierarchy
    organism_class.challenge_rank = challenge_rank
