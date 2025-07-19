import sympy as sp
from core.physics.conversions import ureg

def setup_mechanics_equations(solver):
    """Add all mechanical engineering equations."""
    
    # Add mechanical symbols
    mechanical_symbols = {
        'F': {'units': ureg.newton, 'properties': {'real': True}},
        'F_D': {'units': ureg.newton, 'properties': {'real': True, 'positive': True}},
        'P': {'units': ureg.pascal, 'properties': {'real': True, 'positive': True}},
        'sigma': {'units': ureg.pascal, 'properties': {'real': True, 'positive': True}},
        't': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'sf': {'units': ureg.dimensionless, 'properties': {'real': True, 'positive': True}},
        'rho': {'units': ureg.kilogram/ureg.meter**3, 'properties': {'real': True, 'positive': True}},
        'C_D': {'units': ureg.dimensionless, 'properties': {'real': True, 'positive': True}},
        'v': {'units': ureg.meter/ureg.second, 'properties': {'real': True, 'positive': True}},
    }
    solver.add_symbols(mechanical_symbols)
    
    # Get symbols for equations
    F, P, A = solver.symbols['F'], solver.symbols['P'], solver.symbols['A']
    F_D, rho, C_D, v = solver.symbols['F_D'], solver.symbols['rho'], solver.symbols['C_D'], solver.symbols['v']
    t, d, sigma, sf = solver.symbols['t'], solver.symbols['d'], solver.symbols['sigma'], solver.symbols['sf']
    
    # Add equations
    solver.add_equation('force', sp.Eq(F, P * A))
    solver.add_equation('stress', sp.Eq(sigma, F / A))
    solver.add_equation('kessel', sp.Eq(t, (P * d) / (sigma / sf)))
    solver.add_equation('drag', sp.Eq(F_D, 0.5 * rho * C_D * A * v**2))