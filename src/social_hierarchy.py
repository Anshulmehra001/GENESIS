"""
Social Hierarchy and Roles
Dominance hierarchies and social roles for organisms
"""

class SocialHierarchy:
    """Manages social hierarchy for a group"""
    
    def __init__(self):
        self.members = []
        self.ranks = {}  # organism -> rank (0 = leader, higher = lower rank)
        self.roles = {}  # organism -> role
    
    def add_member(self, organism):
        """Add member to hierarchy"""
        if organism not in self.members:
            self.members.append(organism)
            self.ranks[organism] = len(self.members) - 1
            self.assign_role(organism)
    
    def remove_member(self, organism):
        """Remove member from hierarchy"""
        if organism in self.members:
            self.members.remove(organism)
            if organism in self.ranks:
                del self.ranks[organism]
            if organism in self.roles:
                del self.roles[organism]
    
    def challenge(self, challenger, challenged):
        """Challenge for higher rank"""
        if challenger not in self.members or challenged not in self.members:
            return False
        
        # Success based on energy difference
        if challenger.energy > challenged.energy * 1.2:
            # Swap ranks
            challenger_rank = self.ranks[challenger]
            challenged_rank = self.ranks[challenged]
            self.ranks[challenger] = challenged_rank
            self.ranks[challenged] = challenger_rank
            
            # Reassign roles
            self.assign_role(challenger)
            self.assign_role(challenged)
            return True
        return False
    
    def assign_role(self, organism):
        """Assign role based on rank and traits"""
        rank = self.ranks.get(organism, 999)
        
        if rank == 0:
            self.roles[organism] = 'leader'
        elif rank < len(self.members) * 0.2:
            self.roles[organism] = 'scout'
        elif rank < len(self.members) * 0.5:
            self.roles[organism] = 'guard'
        else:
            self.roles[organism] = 'follower'
    
    def get_role(self, organism):
        """Get organism's role"""
        return self.roles.get(organism, 'follower')
    
    def get_rank(self, organism):
        """Get organism's rank"""
        return self.ranks.get(organism, 999)
    
    def get_leader(self):
        """Get the leader"""
        for organism, rank in self.ranks.items():
            if rank == 0:
                return organism
        return None
    
    def display_behavior(self, organism):
        """Get display behavior based on rank"""
        rank = self.get_rank(organism)
        if rank == 0:
            return 'dominant_display'
        elif rank > len(self.members) * 0.7:
            return 'submissive_display'
        return 'neutral'


class SocialRole:
    """Mixin for organisms with social roles"""
    
    def __init__(self):
        self.role = 'follower'
        self.hierarchy = None
    
    def join_hierarchy(self, hierarchy):
        """Join a social hierarchy"""
        self.hierarchy = hierarchy
        hierarchy.add_member(self)
        self.role = hierarchy.get_role(self)
    
    def leave_hierarchy(self):
        """Leave social hierarchy"""
        if self.hierarchy:
            self.hierarchy.remove_member(self)
            self.hierarchy = None
            self.role = 'follower'
    
    def perform_role_action(self, universe):
        """Perform action based on role"""
        if self.role == 'leader':
            return self.lead_action(universe)
        elif self.role == 'scout':
            return self.scout_action(universe)
        elif self.role == 'guard':
            return self.guard_action(universe)
        else:
            return self.follow_action(universe)
    
    def lead_action(self, universe):
        """Leader makes decisions for group"""
        # Leaders move toward high-energy areas
        return {'priority': 'energy', 'boldness': 1.5}
    
    def scout_action(self, universe):
        """Scout explores new areas"""
        # Scouts move to unexplored areas
        return {'priority': 'explore', 'boldness': 1.2}
    
    def guard_action(self, universe):
        """Guard protects group"""
        # Guards stay near group center
        return {'priority': 'protect', 'boldness': 1.0}
    
    def follow_action(self, universe):
        """Follower follows leader"""
        # Followers stay near leader
        if self.hierarchy:
            leader = self.hierarchy.get_leader()
            if leader:
                return {'priority': 'follow', 'target': leader}
        return {'priority': 'energy', 'boldness': 0.8}
