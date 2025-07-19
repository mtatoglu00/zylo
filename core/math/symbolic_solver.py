import sympy as sp
from typing import Dict, Any, List
from core.physics.conversions import ureg

class SymbolicSolver:
    """
    General equation solver with automatic substitutions.
    No domain-specific knowledge - just pure equation solving.
    """
    
    def __init__(self):
        self.symbols = {}
        self.equations = {}
        self.substitution_rules = {}
        self.unit_map = {}
    
    def add_symbols(self, symbol_definitions: Dict[str, Dict[str, Any]]):
        """Add symbols with units and properties to the solver."""
        for name, definition in symbol_definitions.items():
            properties = definition.get('properties', {'real': True, 'positive': True})
            self.symbols[name] = sp.Symbol(name, **properties)
            self.unit_map[name] = definition.get('units', ureg.dimensionless)
    
    def add_equation(self, name: str, equation: sp.Eq):
        """Add a named equation for solving."""
        self.equations[name] = equation
    
    def add_substitution_rule(self, target: str, sources: List[str], expression: sp.Expr, priority: int = 0):
        """Add rule: target can be calculated from sources using expression."""
        if target not in self.substitution_rules:
            self.substitution_rules[target] = []
        
        self.substitution_rules[target].append({
            'sources': sources,
            'expression': expression,
            'priority': priority
        })
        self.substitution_rules[target].sort(key=lambda x: x['priority'], reverse=True)
    
    def solve_smart(self, equation_name: str, primary_vars: List[str], **kwargs):
        """
        Solve equation with automatic substitutions.
        Provide n-1 variables to solve for the nth.
        
        Args:
            equation_name: Name of equation to solve
            primary_vars: Main variables of the equation
            **kwargs: Known values (including substitution sources)
        """
        known = {k: v for k, v in kwargs.items() if v is not None}
        
        # Find possible substitutions
        possible_subs = self._find_substitutions(equation_name, known)
        
        # Determine what we can effectively solve
        effective_known = set(known.keys()) | set(possible_subs.keys())
        missing = [var for var in primary_vars if var not in effective_known]
        
        if len(missing) != 1:
            raise ValueError(f"Cannot solve. Missing: {missing}, Available subs: {list(possible_subs.keys())}")
        
        return self._solve(equation_name, known, missing[0])
    
    def _find_substitutions(self, equation_name: str, known: Dict[str, Any]) -> Dict[str, sp.Expr]:
        """Find all possible substitutions based on available values."""
        equation = self.equations[equation_name]
        equation_symbols = equation.free_symbols
        possible_subs = {}
        
        for target, rules in self.substitution_rules.items():
            # Skip if target already known or not in equation
            if target in known or self.symbols.get(target) not in equation_symbols:
                continue
            
            # Find first applicable rule
            for rule in rules:
                if all(source in known for source in rule['sources']):
                    possible_subs[target] = rule['expression']
                    break
        
        return possible_subs
    
    def _solve(self, equation_name: str, known: Dict[str, Any], solve_for: str):
        """Core solving logic with substitutions and unit handling."""
        equation = self.equations[equation_name]
        
        # Apply substitutions
        subs = self._find_substitutions(equation_name, known)
        for target, expr in subs.items():
            if target in self.symbols:
                equation = equation.subs(self.symbols[target], expr)
        
        # Convert values to numeric
        substitutions = {}
        for var, value in known.items():
            if var in self.symbols:
                substitutions[self.symbols[var]] = value.to_base_units().magnitude if hasattr(value, 'magnitude') else value
        
        # Solve
        solution = sp.solve(equation.subs(substitutions), self.symbols[solve_for])[0]
        result = float(solution.evalf())
        
        # Apply units
        return result * self.unit_map.get(solve_for, ureg.dimensionless)