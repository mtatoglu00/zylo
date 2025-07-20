import sympy as sp
import logging
from typing import Dict, Any, List
from core.physics.conversions import ureg
from core.data.physics_db import PHYSICS_DB
from core.math.auto_substitution_detector import AutoSubstitutionDetector

class SymbolicSolver:
    """Enhanced solver with automatic substitution detection."""
    
    def __init__(self):
        self.symbols = {}
        self.equations = {}
        self.substitution_rules = {}
        self.unit_map = {}
        self.auto_detector = None
    
    def add_symbols(self, symbol_definitions: Dict[str, Dict[str, Any]]):
        for name, definition in symbol_definitions.items():
            properties = definition.get('properties', {'real': True, 'positive': True})
            self.symbols[name] = sp.Symbol(name, **properties)
            self.unit_map[name] = definition.get('units', ureg.dimensionless)
    
    def add_equation(self, name: str, equation: sp.Eq):
        if equation is not None:
            self.equations[name] = equation
    
    def add_substitution_rule(self, target: str, sources: List[str], expression: sp.Expr, priority: int = 0):
        self.substitution_rules.setdefault(target, []).append({
            'sources': sources,
            'expression': expression,
            'priority': priority
        })
        self.substitution_rules[target].sort(key=lambda x: x['priority'], reverse=True)
    
    def load_from_database(self, domains: List[str] = None):
        if domains is None:
            domains = list(PHYSICS_DB['domains'].keys())
        for domain_name in domains:
            domain = PHYSICS_DB['domains'][domain_name]
            self.add_symbols(self._convert_db_symbols(domain['symbols']))
        for domain_name in domains:
            domain = PHYSICS_DB['domains'][domain_name]
            for eq_name, eq_data in domain['equations'].items():
                eq_str = eq_data if isinstance(eq_data, str) else eq_data['expression']
                self.add_equation(eq_name, self._parse_equation_string(eq_str))
        self.auto_detector = AutoSubstitutionDetector(self)
        for domain_name in domains:
            domain = PHYSICS_DB['domains'][domain_name]
            for eq_name, eq_data in domain['equations'].items():
                if isinstance(eq_data, dict):
                    self.auto_detector.equation_metadata[eq_name] = {k: v for k, v in eq_data.items() if k != 'expression'}
        self.auto_detector.detect_substitutions()
    
    def _convert_db_symbols(self, db_symbols):
        return {name: {'units': self._parse_units(data['units']), 'properties': {'real': True, 'positive': True}}
                for name, data in db_symbols.items()}
    
    def _parse_equation_string(self, eq_string):
        try:
            lhs_str, rhs_str = eq_string.split(' = ')
            namespace = {'pi': sp.pi, 'sp': sp, **self.symbols}
            return sp.Eq(sp.sympify(lhs_str, locals=namespace), sp.sympify(rhs_str, locals=namespace))
        except Exception as e:
            logging.error(f"Failed to parse equation: {eq_string} - {e}")
            return None

    def _parse_units(self, unit_string):
        try:
            return ureg.parse_expression(unit_string)
        except Exception:
            return ureg.dimensionless
    
    def _find_substitutions(self, equation_name: str, known: Dict[str, Any]) -> Dict[str, sp.Expr]:
        equation = self.equations[equation_name]
        equation_symbols = equation.free_symbols
        possible_subs = {}
        calculable = set(known)
        
        # Keep iterating until no new substitutions can be found
        max_iterations = 20  # Prevent infinite loops
        for iteration in range(max_iterations):
            changed = False
            
            for target, rules in self.substitution_rules.items():
                if target in calculable:
                    continue
                
                # Try each rule for this target
                for rule in rules:
                    if all(source in calculable for source in rule['sources']):
                        possible_subs[target] = rule['expression']
                        calculable.add(target)
                        changed = True
                        break
            
            if not changed:
                break
                
        return possible_subs

    def solve_smart(self, equation_name: str, primary_vars: List[str], **kwargs):
        known = {k: v for k, v in kwargs.items() if v is not None}
        
        # Get all possible substitutions through deep chaining
        possible_subs = self._find_substitutions(equation_name, known)
        
        # Calculate what we can effectively solve
        effective_known = set(known) | set(possible_subs)
        truly_missing = [var for var in primary_vars if var not in effective_known]
        
        if len(truly_missing) > 1:
            raise ValueError(f"Cannot solve. Missing: {truly_missing}, Available subs: {list(possible_subs)}, Known: {list(known)}")
        
        # Determine what to solve for
        if len(truly_missing) == 1:
            solve_for = truly_missing[0]
        else:
            # All variables can be determined - pick the best target
            solve_candidates = [var for var in primary_vars if var not in known]
            solve_for = solve_candidates[0] if len(solve_candidates) == 1 else self._determine_best_solve_target(equation_name, solve_candidates, known, possible_subs)
        
        if solve_for is None:
            raise ValueError(f"Cannot determine what to solve for in equation '{equation_name}'")
            
        return self._solve(equation_name, known, solve_for)

    def _determine_best_solve_target(self, equation_name: str, candidates: List[str], known: Dict, possible_subs: Dict) -> str:
        non_substitutable = [var for var in candidates if var not in possible_subs]
        if len(non_substitutable) == 1:
            return non_substitutable[0]
        metadata = self.auto_detector.equation_metadata.get(equation_name)
        if metadata and 'output' in metadata and metadata['output'] in candidates:
            return metadata['output']
        result_unit_patterns = ['newton', 'pascal', 'watt', 'joule', 'dimensionless']
        for candidate in candidates:
            candidate_units = str(self.unit_map.get(candidate, ''))
            if any(pattern in candidate_units for pattern in result_unit_patterns):
                return candidate
        return candidates[0] if candidates else None
    
    def _solve(self, equation_name: str, known: Dict[str, Any], solve_for: str):
        equation = self.equations[equation_name]
        substituted_eq = equation
        possible_subs = self._find_substitutions(equation_name, known)
        for _ in range(10):
            changed = False
            for var, sub_expr in possible_subs.items():
                if var != solve_for:
                    old_eq = substituted_eq
                    substituted_eq = substituted_eq.subs(self.symbols[var], sub_expr)
                    if substituted_eq != old_eq:
                        changed = True
            if not changed:
                break
        for var, value in known.items():
            if var in self.symbols:
                # Convert to SI base units before extracting magnitude
                if hasattr(value, 'to_base_units'):
                    substituted_eq = substituted_eq.subs(self.symbols[var], value.to_base_units().magnitude)
                else:
                    substituted_eq = substituted_eq.subs(self.symbols[var], value)
        target_symbol = self.symbols[solve_for]
        solutions = sp.solve(substituted_eq, target_symbol)
        if not solutions:
            raise ValueError(
                f"No solution found for '{solve_for}' in equation '{equation_name}'.\n"
                f"Equation: {equation}\n"
                f"Known inputs: {known}"
            )
        try:
            result = float(solutions[0].evalf())
        except Exception:
            result = float(sp.simplify(solutions[0]).evalf())
        if solve_for in self.unit_map:
            result = result * self.unit_map[solve_for]
        return result