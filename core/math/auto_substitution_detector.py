import sympy as sp
from typing import Dict, List

class AutoSubstitutionDetector:
    """Automatically detect substitution rules from equation metadata."""
    
    def __init__(self, solver):
        self.solver = solver
        self.equation_metadata = {}
    
    def detect_substitutions(self):
        """Auto-detect substitution rules using equation metadata."""
        for eq_name, equation in self.solver.equations.items():
            metadata = self.equation_metadata.get(eq_name)
            
            if metadata:
                self._create_substitution_from_metadata(eq_name, equation, metadata)
            else:
                self._generic_substitution_detection(eq_name, equation)
    
    def _create_substitution_from_metadata(self, eq_name, equation, metadata):
        """Create substitution rules using explicit metadata."""
        
        if metadata.get('bidirectional'):
            self._create_bidirectional_substitution(equation)
        elif 'output' in metadata and 'inputs' in metadata:
            self._create_unidirectional_substitution(equation, metadata['output'], metadata['inputs'])
        else:
            self._generic_substitution_detection(eq_name, equation)
    
    def _create_bidirectional_substitution(self, equation):
        """Create bidirectional substitution for equations marked as bidirectional."""
        symbols = equation.free_symbols
        symbol_names = [str(sym) for sym in symbols]
        
        # For bidirectional equations, try to solve for each variable
        for target in symbol_names:
            other_symbols = [s for s in symbol_names if s != target]
            self._create_substitution_rule(equation, target, other_symbols)
    
    def _create_unidirectional_substitution(self, equation, output, inputs):
        """Create unidirectional substitution rule."""
        self._create_substitution_rule(equation, output, inputs)
    
    def _create_substitution_rule(self, equation, target, sources):
        """Generic substitution rule creation."""
        try:
            if target not in self.solver.symbols:
                return
                
            target_sym = self.solver.symbols[target]
            solution = sp.solve(equation, target_sym)
            
            if not solution:
                return
                
            priority = 20 - len(sources)  # Fewer sources = higher priority
            
            self.solver.add_substitution_rule(
                target=target,
                sources=sources,
                expression=solution[0],
                priority=priority
            )
            
        except Exception:
            pass
    
    def _generic_substitution_detection(self, eq_name, equation):
        """Generic detection for equations without metadata."""
        symbols = equation.free_symbols
        symbol_names = [str(sym) for sym in symbols]
        
        if len(symbols) == 2:
            self._create_bidirectional_substitution(equation)
        elif len(symbols) > 2:
            self._analyze_symbol_roles(equation, symbol_names, eq_name)
    
    def _analyze_symbol_roles(self, equation, symbol_names, eq_name):
        """Analyze equation structure to determine input/output roles."""
        # Try each symbol as output
        for symbol in symbol_names:
            other_symbols = [s for s in symbol_names if s != symbol]
            try:
                self._create_substitution_rule(equation, symbol, other_symbols)
            except:
                continue