from core.math.symbolic_solver import SymbolicSolver

class mechanics:
    """Physics calculator with automatic equation solving."""
    
    def __init__(self, name: str = ''):
        self.name = name
        self.solver = SymbolicSolver()
        self.solver.load_from_database(['geometry', 'mechanics', 'fluids'])
    
    def solve(self, equation_name: str, **kwargs):
        """Generic solve method - works for any equation."""
        equation = self.solver.equations[equation_name]
        primary_vars = [str(sym) for sym in equation.free_symbols]
        return self.solver.solve_smart(equation_name, primary_vars, **kwargs)