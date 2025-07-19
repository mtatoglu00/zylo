import sympy as sp
from core.physics.conversions import ureg

def setup_fluid_equations(solver):
    """Add fluid mechanics equations."""
    
    # Add fluid symbols
    fluid_symbols = {
        'Q': {'units': ureg.meter**3/ureg.second, 'properties': {'real': True, 'positive': True}},  # Flow rate
        'mu': {'units': ureg.pascal*ureg.second, 'properties': {'real': True, 'positive': True}},   # Viscosity
        'Re': {'units': ureg.dimensionless, 'properties': {'real': True, 'positive': True}},        # Reynolds number
    }
    solver.add_symbols(fluid_symbols)
    
    # Get symbols
    Q, A, v = solver.symbols['Q'], solver.symbols['A'], solver.symbols['v']
    Re, rho, mu, d = solver.symbols['Re'], solver.symbols['rho'], solver.symbols['mu'], solver.symbols['d']
    
    # Add equations
    solver.add_equation('flow_rate', sp.Eq(Q, A * v))  # Q = A × v
    solver.add_equation('reynolds', sp.Eq(Re, (rho * v * d) / mu))  # Re = ρvd/μ