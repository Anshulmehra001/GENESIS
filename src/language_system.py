"""
Phase 4: Language Emergence System
Implements symbolic communication, grammar, meaning negotiation
"""

import random
from collections import defaultdict, Counter

class Symbol:
    """A symbolic unit of language"""
    def __init__(self, form, meaning=None):
        self.form = form  # The symbol itself (string/number)
        self.meaning = meaning  # What it refers to
        self.usage_count = 0
        self.contexts = []  # Contexts where used
        self.associations = {}  # Other symbols it appears with
    
    def use(self, context):
        """Record usage"""
        self.usage_count += 1
        self.contexts.append(context)
    
    def associate_with(self, other_symbol):
        """Record co-occurrence"""
        if other_symbol.form not in self.associations:
            self.associations[other_symbol.form] = 0
        self.associations[other_symbol.form] += 1

class Utterance:
    """A sequence of symbols"""
    def __init__(self, symbols, meaning=None):
        self.symbols = symbols  # List of Symbol objects
        self.meaning = meaning  # Intended meaning
        self.timestamp = 0
        self.speaker = None
        self.listeners = []
    
    def __str__(self):
        return ' '.join([s.form for s in self.symbols])

class Grammar:
    """Emergent grammatical rules"""
    def __init__(self):
        self.rules = []  # (pattern, frequency)
        self.word_order = defaultdict(int)  # Track common orders
        self.combinations = defaultdict(int)  # Valid combinations
    
    def observe(self, utterance):
        """Learn from utterance"""
        symbols = [s.form for s in utterance.symbols]
        
        # Learn word order
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i+1])
            self.word_order[pair] += 1
        
        # Learn valid combinations
        pattern = tuple(symbols)
        self.combinations[pattern] += 1
    
    def is_valid(self, utterance):
        """Check if utterance follows grammar"""
        symbols = [s.form for s in utterance.symbols]
        
        # Check word order
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i+1])
            if pair in self.word_order:
                return True
        
        # Check if pattern seen before
        pattern = tuple(symbols)
        return pattern in self.combinations
    
    def generate(self, start_symbol):
        """Generate grammatical utterance"""
        result = [start_symbol]
        
        # Follow most common patterns
        for _ in range(3):  # Max length
            current = result[-1]
            # Find most common next symbol
            next_symbols = [(pair[1], count) for pair, count in self.word_order.items() 
                          if pair[0] == current]
            if next_symbols:
                next_sym = max(next_symbols, key=lambda x: x[1])[0]
                result.append(next_sym)
            else:
                break
        
        return result

class Lexicon:
    """Vocabulary of symbols"""
    def __init__(self):
        self.symbols = {}  # form -> Symbol
        self.meanings = {}  # meaning -> Symbol
        self.next_id = 0
    
    def create_symbol(self, meaning=None):
        """Invent new symbol"""
        form = f"sym_{self.next_id}"
        self.next_id += 1
        
        symbol = Symbol(form, meaning)
        self.symbols[form] = symbol
        
        if meaning:
            self.meanings[meaning] = symbol
        
        return symbol
    
    def get_symbol(self, form):
        """Retrieve symbol"""
        return self.symbols.get(form)
    
    def get_meaning(self, meaning):
        """Find symbol for meaning"""
        return self.meanings.get(meaning)
    
    def negotiate_meaning(self, symbol, new_meaning, strength=0.1):
        """Meaning can drift over time"""
        if symbol.form in self.symbols:
            # Blend old and new meaning
            # In real system, this would be more sophisticated
            symbol.meaning = new_meaning
            self.meanings[new_meaning] = symbol

class LanguageSystem:
    """Language capabilities for organisms"""
    
    def __init__(self, organism):
        self.organism = organism
        
        # Personal lexicon
        self.lexicon = Lexicon()
        
        # Grammar knowledge
        self.grammar = Grammar()
        
        # Communication history
        self.utterances_produced = []
        self.utterances_heard = []
        
        # Shared language (population-level)
        self.dialect = None  # Reference to shared dialect
        
        # Language learning
        self.learning_rate = 0.1
        self.innovation_rate = 0.01  # Chance to invent new symbol
    
    def express(self, meaning):
        """Create utterance to express meaning"""
        # Try to find existing symbol
        symbol = self.lexicon.get_meaning(meaning)
        
        # If no symbol exists, maybe invent one
        if not symbol and random.random() < self.innovation_rate:
            symbol = self.lexicon.create_symbol(meaning)
        
        if not symbol:
            return None
        
        # Create simple utterance (single symbol for now)
        utterance = Utterance([symbol], meaning)
        utterance.speaker = self.organism
        
        # Record production
        self.utterances_produced.append(utterance)
        symbol.use(meaning)
        
        # Learn grammar from own production
        self.grammar.observe(utterance)
        
        return utterance
    
    def compose(self, meanings):
        """Compose multi-symbol utterance"""
        symbols = []
        
        for meaning in meanings:
            symbol = self.lexicon.get_meaning(meaning)
            if not symbol:
                # Invent if needed
                if random.random() < self.innovation_rate:
                    symbol = self.lexicon.create_symbol(meaning)
            
            if symbol:
                symbols.append(symbol)
        
        if not symbols:
            return None
        
        # Create compositional utterance
        utterance = Utterance(symbols, meanings)
        utterance.speaker = self.organism
        
        # Record and learn
        self.utterances_produced.append(utterance)
        self.grammar.observe(utterance)
        
        # Learn associations between symbols
        for i in range(len(symbols) - 1):
            symbols[i].associate_with(symbols[i+1])
        
        return utterance
    
    def comprehend(self, utterance):
        """Understand received utterance"""
        self.utterances_heard.append(utterance)
        
        # Learn from observation
        self.grammar.observe(utterance)
        
        # Try to infer meaning
        meanings = []
        for symbol in utterance.symbols:
            # Check if we know this symbol
            known_symbol = self.lexicon.get_symbol(symbol.form)
            
            if known_symbol:
                # We know it!
                meanings.append(known_symbol.meaning)
            else:
                # Learn new symbol
                if random.random() < self.learning_rate:
                    # Copy symbol to our lexicon
                    new_symbol = Symbol(symbol.form, symbol.meaning)
                    self.lexicon.symbols[symbol.form] = new_symbol
                    if symbol.meaning:
                        self.lexicon.meanings[symbol.meaning] = new_symbol
                    meanings.append(symbol.meaning)
        
        return meanings
    
    def negotiate(self, other_organism, symbol_form):
        """Negotiate meaning with another organism"""
        my_symbol = self.lexicon.get_symbol(symbol_form)
        their_symbol = other_organism.language.lexicon.get_symbol(symbol_form)
        
        if not my_symbol or not their_symbol:
            return False
        
        # If meanings differ, negotiate
        if my_symbol.meaning != their_symbol.meaning:
            # Simple negotiation: more experienced wins
            if my_symbol.usage_count > their_symbol.usage_count:
                # They adopt my meaning
                other_organism.language.lexicon.negotiate_meaning(
                    their_symbol, my_symbol.meaning
                )
            else:
                # I adopt their meaning
                self.lexicon.negotiate_meaning(
                    my_symbol, their_symbol.meaning
                )
            return True
        
        return False
    
    def innovate(self):
        """Spontaneously create new symbol"""
        # Invent symbol for common experience
        common_meanings = ['food', 'danger', 'friend', 'home', 'tool']
        meaning = random.choice(common_meanings)
        
        # Only if we don't have one already
        if not self.lexicon.get_meaning(meaning):
            symbol = self.lexicon.create_symbol(meaning)
            return symbol
        
        return None
    
    def teach(self, other_organism, meaning):
        """Teach symbol to another organism"""
        symbol = self.lexicon.get_meaning(meaning)
        if not symbol:
            return False
        
        # Create teaching utterance
        utterance = Utterance([symbol], meaning)
        utterance.speaker = self.organism
        utterance.listeners = [other_organism]
        
        # Other organism learns
        other_organism.language.comprehend(utterance)
        
        return True
    
    def get_vocabulary_size(self):
        """Count known symbols"""
        return len(self.lexicon.symbols)
    
    def get_grammar_complexity(self):
        """Measure grammar sophistication"""
        return len(self.grammar.combinations)
    
    def get_stats(self):
        """Get language statistics"""
        return {
            'vocabulary_size': self.get_vocabulary_size(),
            'grammar_rules': len(self.grammar.word_order),
            'utterances_produced': len(self.utterances_produced),
            'utterances_heard': len(self.utterances_heard),
            'innovations': sum(1 for s in self.lexicon.symbols.values() 
                             if s.usage_count == 0)
        }

class Dialect:
    """Shared language of a population"""
    def __init__(self):
        self.shared_lexicon = Lexicon()
        self.shared_grammar = Grammar()
        self.speakers = []
        self.age = 0  # How long dialect has existed
    
    def add_speaker(self, organism):
        """Organism joins dialect community"""
        self.speakers.append(organism)
        organism.language.dialect = self
    
    def evolve(self):
        """Language changes over time"""
        self.age += 1
        
        # Collect innovations from speakers
        for speaker in self.speakers:
            for symbol in speaker.language.lexicon.symbols.values():
                if symbol.usage_count > 5:  # Popular symbol
                    # Add to shared lexicon
                    if symbol.form not in self.shared_lexicon.symbols:
                        self.shared_lexicon.symbols[symbol.form] = symbol
                        if symbol.meaning:
                            self.shared_lexicon.meanings[symbol.meaning] = symbol
        
        # Meaning drift
        if random.random() < 0.01:
            # Random symbol changes meaning slightly
            if self.shared_lexicon.symbols:
                symbol = random.choice(list(self.shared_lexicon.symbols.values()))
                # Meaning drifts (simplified)
                symbol.meaning = f"{symbol.meaning}_evolved"
