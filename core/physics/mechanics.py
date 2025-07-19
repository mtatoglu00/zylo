from core.math.symbolic_solver import SymbolicSolver
from core.rules.geometry_rules import setup_geometry_rules, setup_density_rules
from core.equations.mechanics_equations import setup_mechanics_equations
from core.equations.fluid_equations import setup_fluid_equations

class mechanics:
    """Clean mechanics class - just a thin wrapper around SymbolicSolver."""
    
    def __init__(self, name: str = ''):
        self.name = name
        self.solver = SymbolicSolver()
        
        # Setup all rules and equations
        setup_geometry_rules(self.solver)
        setup_density_rules(self.solver)
        setup_mechanics_equations(self.solver)
        setup_fluid_equations(self.solver)
    
    def force(self, **kwargs):
        """Calculate force: F = P × A"""
        return self.solver.solve_smart('force', ['F', 'P', 'A'], **kwargs)
    
    def stress(self, **kwargs):
        """Calculate stress: σ = F / A"""
        return self.solver.solve_smart('stress', ['sigma', 'F', 'A'], **kwargs)
    
    def drag_force(self, **kwargs):
        """Calculate drag force: F_D = ½ρC_DA v²"""
        return self.solver.solve_smart('drag', ['F_D', 'rho', 'C_D', 'A', 'v'], **kwargs)
    
    def kessel_formula(self, **kwargs):
        """Calculate pressure vessel thickness"""
        known = {k: v for k, v in kwargs.items() if v is not None}
        if len(known) != 4:
            raise ValueError("Provide exactly 4 parameters for Kessel formula")
        return self.solver.solve_smart('kessel', ['t', 'P', 'd', 'sigma', 'sf'], **kwargs)
    
    # For testing purposes only
    def flow_rate(self, **kwargs):
        """Calculate flow rate: Q = A × v"""
        return self.solver.solve_smart('flow_rate', ['Q', 'A', 'v'], **kwargs)
    
    def reynolds_number(self, **kwargs):
        """Calculate Reynolds number: Re = ρvd/μ"""
        return self.solver.solve_smart('reynolds', ['Re', 'rho', 'v', 'd', 'mu'], **kwargs)


