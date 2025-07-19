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
        """Add symbols with units and properties to the solver."""
        for name, definition in symbol_definitions.items():
            properties = definition.get('properties', {'real': True, 'positive': True})
            self.symbols[name] = sp.Symbol(name, **properties)
            self.unit_map[name] = definition.get('units', ureg.dimensionless)
    
    def add_equation(self, name: str, equation: sp.Eq):
        """Add a named equation for solving."""
        if equation is not None:
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
    
    def load_from_database(self, domains: List[str] = None):
        """Load symbols and equations from database and auto-detect substitutions."""
        
        if domains is None:
            domains = list(PHYSICS_DB['domains'].keys())
        
        # Load symbols first
        for domain_name in domains:
            domain = PHYSICS_DB['domains'][domain_name]
            symbols = self._convert_db_symbols(domain['symbols'])
            self.add_symbols(symbols)
        
        # Load equations
        for domain_name in domains:
            domain = PHYSICS_DB['domains'][domain_name]
            equations_data = domain['equations']
            for eq_name, eq_data in equations_data.items():
                if isinstance(eq_data, str):
                    equation = self._parse_equation_string(eq_data)
                else:
                    equation = self._parse_equation_string(eq_data['expression'])
                
                self.add_equation(eq_name, equation)
        
        # Auto-detect substitution rules
        self.auto_detector = AutoSubstitutionDetector(self)
        
        # Pass metadata to auto-detector
        for domain_name in domains:
            domain = PHYSICS_DB['domains'][domain_name]
            equations_data = domain['equations']
            for eq_name, eq_data in equations_data.items():
                if isinstance(eq_data, dict):
                    metadata = {k: v for k, v in eq_data.items() if k != 'expression'}
                    self.auto_detector.equation_metadata[eq_name] = metadata
        
        self.auto_detector.detect_substitutions()
    
    def _convert_db_symbols(self, db_symbols):
        """Convert database symbol format to solver format."""
        converted = {}
        for name, data in db_symbols.items():
            converted[name] = {
                'units': self._parse_units(data['units']),
                'properties': {'real': True, 'positive': True}
            }
        return converted
    
    def _parse_equation_string(self, eq_string):
        """Convert database equation strings to SymPy equations."""
        try:
            lhs_str, rhs_str = eq_string.split(' = ')
            
            namespace = {
                'pi': sp.pi,
                'sp': sp,
                **self.symbols
            }
            
            lhs_expr = sp.sympify(lhs_str, locals=namespace)
            rhs_expr = sp.sympify(rhs_str, locals=namespace)
            
            return sp.Eq(lhs_expr, rhs_expr)
            
        except Exception as e:
            logging.error(f"Failed to parse equation: {eq_string} - {e}")
            return None

    def _parse_units(self, unit_string):
        """Convert unit string to pint unit."""
        try:
            return ureg.parse_expression(unit_string)
        except:
            try:
                normalized = unit_string.replace('**', '^')
                return ureg.parse_expression(normalized)
            except:
                return ureg.dimensionless
    
    def solve_smart(self, equation_name: str, primary_vars: List[str], **kwargs):
        """Solve equation with automatic substitutions."""
        known = {k: v for k, v in kwargs.items() if v is not None}
        
        # Find possible substitutions first
        possible_subs = self._find_substitutions(equation_name, known)
        
        # Determine what we can effectively solve (known + substitutable)
        effective_known = set(known.keys()) | set(possible_subs.keys())
        
        # Find variables that are truly missing (can't be calculated)
        truly_missing = [var for var in primary_vars if var not in effective_known]
        
        if len(truly_missing) == 0:
            # All variables can be calculated - need to determine target
            # Look for variables that are NOT provided directly (these are solve targets)
            solve_candidates = [var for var in primary_vars if var not in known]
            
            if len(solve_candidates) == 1:
                solve_for = solve_candidates[0]
            else:
                # Multiple candidates - use equation metadata or heuristics
                solve_for = self._determine_best_solve_target(equation_name, solve_candidates, known, possible_subs)
                
        elif len(truly_missing) == 1:
            # Perfect - exactly one variable we can't calculate
            solve_for = truly_missing[0]
        else:
            # Multiple missing variables - can't solve
            raise ValueError(f"Cannot solve. Missing: {truly_missing}, Available subs: {list(possible_subs.keys())}")
        
        if solve_for is None:
            raise ValueError(f"Cannot determine what to solve for in equation '{equation_name}'")
        
        return self._solve(equation_name, known, solve_for)

    def _determine_best_solve_target(self, equation_name: str, candidates: List[str], known: Dict, possible_subs: Dict) -> str:
        """Determine the best variable to solve for when multiple options exist."""
        
        # Priority 1: Variables that can't be substituted (must be solved directly)
        non_substitutable = [var for var in candidates if var not in possible_subs]
        if len(non_substitutable) == 1:
            return non_substitutable[0]
        
        # Priority 2: Use equation metadata if available
        if hasattr(self, 'auto_detector') and self.auto_detector:
            metadata = self.auto_detector.equation_metadata.get(equation_name)
            if metadata and 'output' in metadata and metadata['output'] in candidates:
                return metadata['output']
        
        # Priority 3: Prefer variables with complex units (likely outputs)
        result_unit_patterns = ['newton', 'pascal', 'watt', 'joule', 'dimensionless']
        
        for candidate in candidates:
            candidate_units = str(self.unit_map.get(candidate, ''))
            if any(pattern in candidate_units for pattern in result_unit_patterns):
                return candidate
        
        # Priority 4: Return first candidate
        return candidates[0] if candidates else None
    
    def _find_substitutions(self, equation_name: str, known: Dict[str, Any]) -> Dict[str, sp.Expr]:
        """Find all possible substitutions based on available values with recursive detection."""
        equation = self.equations[equation_name]
        equation_symbols = equation.free_symbols
        possible_subs = {}
        
        # Keep track of what we can calculate (including through substitution chains)
        calculable = set(known.keys())
        
        # Iteratively find substitutions until no new ones are found
        changed = True
        while changed:
            changed = False
            
            for target, rules in self.substitution_rules.items():
                # Skip if target already known or calculated
                if target in calculable:
                    continue
                    
                # Check if target is needed (either in equation or for other substitutions)
                target_needed = (
                    self.symbols.get(target) in equation_symbols or  # Direct use in equation
                    self._is_intermediate_variable_needed(target, equation_symbols, calculable)  # Intermediate use
                )
                
                if not target_needed:
                    continue
                
                # Find first applicable rule
                for rule in rules:
                    if all(source in calculable for source in rule['sources']):
                        possible_subs[target] = rule['expression']
                        calculable.add(target)
                        changed = True
                        break
    
        return possible_subs

    def _is_intermediate_variable_needed(self, target: str, equation_symbols: set, calculable: set) -> bool:
        """Check if a variable is needed as an intermediate for other substitutions."""
        # Check if any other substitution rule needs this target as a source
        for other_target, rules in self.substitution_rules.items():
            # Skip if other_target already calculable
            if other_target in calculable:
                continue
                
            # Check if other_target is in equation or could lead to equation variables
            if self.symbols.get(other_target) in equation_symbols:
                for rule in rules:
                    if target in rule['sources']:
                        return True
    
        return False

    def _solve(self, equation_name: str, known: Dict[str, Any], solve_for: str):
        """Solve equation with substitutions."""
        equation = self.equations[equation_name]
        
        # Apply substitutions with recursive substitution
        substituted_eq = equation
        possible_subs = self._find_substitutions(equation_name, known)
        
        # RECURSIVE SUBSTITUTION: Keep substituting until no more changes
        max_iterations = 10
        for iteration in range(max_iterations):
            changed = False
            for var, sub_expr in possible_subs.items():
                if var != solve_for:  # Don't substitute the variable we're solving for
                    old_eq = substituted_eq
                    substituted_eq = substituted_eq.subs(self.symbols[var], sub_expr)
                    if substituted_eq != old_eq:
                        changed = True
        
            if not changed:
                break

        # Apply known values
        for var, value in known.items():
            if var in self.symbols:
                substituted_eq = substituted_eq.subs(self.symbols[var], value.magnitude if hasattr(value, 'magnitude') else value)

        # Solve for target variable
        target_symbol = self.symbols[solve_for]
        solutions = sp.solve(substituted_eq, target_symbol)
        
        # Check if we found solutions
        if not solutions:
            raise ValueError(
                f"No solution found for '{solve_for}' in equation '{equation_name}'.\n"
                f"Equation: {equation}\n"
                f"Known inputs: {known}"
            )
        
        # NUMERICAL EVALUATION: Force evaluation to float
        try:
            result = float(solutions[0].evalf())
        except (TypeError, ValueError):
            # Try simplification if direct conversion fails
            simplified = sp.simplify(solutions[0])
            result = float(simplified.evalf())

        # Apply units
        if solve_for in self.unit_map:
            result = result * self.unit_map[solve_for]

        return result