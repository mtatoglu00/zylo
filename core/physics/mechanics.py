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
    
    # Convenience methods
    def force(self, **kwargs):
        """Calculate force: F = P × A"""
        return self.solver.solve_smart('force', ['F', 'P', 'A'], **kwargs)
    
    def drag_force(self, **kwargs):
        """Calculate drag force: F_D = ½ρC_DA v²"""
        return self.solver.solve_smart('drag', ['F_D', 'rho', 'C_D', 'A', 'v'], **kwargs)
    
    def stress(self, **kwargs):
        """Calculate stress: σ = F / A"""
        return self.solver.solve_smart('stress', ['sigma', 'F', 'A'], **kwargs)
    
    def flow_rate(self, **kwargs):
        """Calculate flow rate: Q = A × v"""
        return self.solver.solve_smart('flow_rate', ['Q', 'A', 'v'], **kwargs)
    
    def reynolds_number(self, **kwargs):
        """Calculate Reynolds number: Re = ρvD/μ"""  # Updated comment
        return self.solver.solve_smart('reynolds', ['Re', 'rho', 'v', 'D', 'mu'], **kwargs)  # Changed 'd' to 'D'


