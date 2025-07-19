import sympy as sp
from core.physics.conversions import ureg

def setup_geometry_rules(solver):
    """
    Add geometric symbols and substitution rules.
    Covers circles, rectangles, triangles, rings, ellipses, volumes.
    """
    
    # Add geometric symbols
    geometric_symbols = {
        'r': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'l': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'w': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'h': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'd': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'A': {'units': ureg.meter**2, 'properties': {'real': True, 'positive': True}},
        'V': {'units': ureg.meter**3, 'properties': {'real': True, 'positive': True}},
        # Add all the complex shapes
        'r_outer': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'r_inner': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
        'a': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},  # Semi-major
        'b': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},  # Semi-minor
        'theta': {'units': ureg.radian, 'properties': {'real': True, 'positive': True}},
    }
    solver.add_symbols(geometric_symbols)
    
    # Add shape substitution rules
    solver.add_substitution_rule('A', ['r'], sp.pi * solver.symbols['r']**2)
    solver.add_substitution_rule('A', ['l', 'w'], solver.symbols['l'] * solver.symbols['w'])
    solver.add_substitution_rule('A', ['d'], sp.pi * (solver.symbols['d']/2)**2)
    solver.add_substitution_rule('A', ['l', 'h'], 0.5 * solver.symbols['l'] * solver.symbols['h'])  # Triangle
    
    # Complex shapes
    solver.add_substitution_rule('A', ['r_outer', 'r_inner'], 
                                sp.pi * (solver.symbols['r_outer']**2 - solver.symbols['r_inner']**2))  # Ring
    solver.add_substitution_rule('A', ['a', 'b'], 
                                sp.pi * solver.symbols['a'] * solver.symbols['b'])  # Ellipse
    solver.add_substitution_rule('A', ['r', 'theta'], 
                                0.5 * solver.symbols['r']**2 * solver.symbols['theta'])  # Sector
    
    # Volume rules
    solver.add_substitution_rule('V', ['r', 'h'], sp.pi * solver.symbols['r']**2 * solver.symbols['h'])
    solver.add_substitution_rule('V', ['l', 'w', 'h'], solver.symbols['l'] * solver.symbols['w'] * solver.symbols['h'])
    
    # Diameter/radius conversions
    solver.add_substitution_rule('r', ['d'], solver.symbols['d']/2)
    solver.add_substitution_rule('d', ['r'], 2 * solver.symbols['r'])

def setup_density_rules(solver):
    """Add density substitution rules: ρ = m/V and m = ρ×V."""
    
    # Add density symbols
    density_symbols = {
        'm': {'units': ureg.kilogram, 'properties': {'real': True, 'positive': True}},
        'rho': {'units': ureg.kilogram/ureg.meter**3, 'properties': {'real': True, 'positive': True}}
    }
    solver.add_symbols(density_symbols)
    
    # Add density substitution rules
    solver.add_substitution_rule('rho', ['m', 'V'], solver.symbols['m'] / solver.symbols['V'])
    solver.add_substitution_rule('m', ['rho', 'V'], solver.symbols['rho'] * solver.symbols['V'])