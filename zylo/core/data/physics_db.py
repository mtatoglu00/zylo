"""
Physics database - all equations and symbols in one place.
This will eventually become a real database.
"""

PHYSICS_DB = {
    'domains': {
        'geometry': {
            'symbols': {
                'r': {'units': 'meter', 'description': 'Radius'},
                'l': {'units': 'meter', 'description': 'Length'},
                'w': {'units': 'meter', 'description': 'Width'},
                'h': {'units': 'meter', 'description': 'Height'},
                'd': {'units': 'meter', 'description': 'Diameter'},
                'A': {'units': 'meter**2', 'description': 'Area'},
                'V': {'units': 'meter**3', 'description': 'Volume'},
                'r_outer': {'units': 'meter', 'description': 'Outer radius'},
                'r_inner': {'units': 'meter', 'description': 'Inner radius'},
                'a': {'units': 'meter', 'description': 'Semi-major axis'},
                'b': {'units': 'meter', 'description': 'Semi-minor axis'},
                'theta': {'units': 'radian', 'description': 'Angle'},
                'm': {'units': 'kilogram', 'description': 'Mass'},
                'rho': {'units': 'kilogram/meter**3', 'description': 'Density'},
                'L': {'units': 'meter', 'description': 'Length'},  # Add this for beam equations
            },
            'equations': {
                'circle_area': {
                    'expression': 'A = pi * r**2',
                    'bidirectional': True
                },
                'rectangle_area': {
                    'expression': 'A = l * w',
                    'output': 'A',
                    'inputs': ['l', 'w']
                },
                'triangle_area': {
                    'expression': 'A = 0.5 * l * h',
                    'output': 'A',
                    'inputs': ['l', 'h']
                },
                'ring_area': {
                    'expression': 'A = pi * (r_outer**2 - r_inner**2)',
                    'output': 'A',
                    'inputs': ['r_outer', 'r_inner']
                },
                'ellipse_area': {
                    'expression': 'A = pi * a * b',
                    'output': 'A',
                    'inputs': ['a', 'b']
                },
                'sector_area': {
                    'expression': 'A = 0.5 * r**2 * theta',
                    'output': 'A',
                    'inputs': ['r', 'theta']
                },
                'cylinder_volume': {
                    'expression': 'V = pi * r**2 * h',
                    'output': 'V',
                    'inputs': ['r', 'h']
                },
                'box_volume': {
                    'expression': 'V = l * w * h',
                    'output': 'V',
                    'inputs': ['l', 'w', 'h']
                },
                'diameter': {
                    'expression': 'd = 2 * r',
                    'bidirectional': True
                },
                'density': {
                    'expression': 'rho = m / V',
                    'output': 'rho',
                    'inputs': ['m', 'V']
                },
            }
        },
        
        'mechanics': {
            'symbols': {
                'F': {'units': 'newton', 'description': 'Force'},
                'F_D': {'units': 'newton', 'description': 'Drag force'},
                'P': {'units': 'pascal', 'description': 'Pressure'},
                'sigma': {'units': 'pascal', 'description': 'Stress'},
                't': {'units': 'meter', 'description': 'Thickness'},
                'C_D': {'units': 'dimensionless', 'description': 'Drag coefficient'},
                'v': {'units': 'meter/second', 'description': 'Velocity'},
                'delta': {'units': 'meter', 'description': 'Deflection'},
                'E': {'units': 'pascal', 'description': 'Young\'s modulus'},
                'I': {'units': 'meter**4', 'description': 'Second moment of area'},
                'b': {'units': 'meter', 'description': 'Beam width'},
                'h': {'units': 'meter', 'description': 'Beam height'},
                'yield_strength': {'units': 'pascal', 'description': 'Yield strength'},
                'safety_factor': {'units': 'dimensionless', 'description': 'Safety factor'},
                'sigma_allow': {'units': 'pascal', 'description': 'Allowable stress'},
            },
            'equations': {
                'force': {
                    'expression': 'F = P * A',
                    'bidirectional': True
                },
                'stress': {
                    'expression': 'sigma = F / A',
                    'output': 'sigma',
                    'inputs': ['F', 'A']
                },
                'kessel': {
                    'expression': 't = (P * d) / (2 * sigma_allow)',
                    'output': 't',
                    'inputs': ['P', 'd', 'sigma_allow']
                },
                'drag': {
                    'expression': 'F_D = 0.5 * rho * C_D * A * v**2',
                    'output': 'F_D',
                    'inputs': ['rho', 'C_D', 'A', 'v']
                },
                'beam_deflection': {
                    'expression': 'delta = (F * L**3) / (48 * E * I)',
                    'output': 'delta',
                    'inputs': ['F', 'L', 'E', 'I']
                },
                'second_moment_rect': {
                    'expression': 'I = (b * h**3) / 12',
                    'output': 'I',
                    'inputs': ['b', 'h']
                },
                'sigma_allow': {
                    'expression': 'sigma_allow = yield_strength / safety_factor',
                    'output': 'sigma_allow',
                    'inputs': ['yield_strength', 'safety_factor']
                },
            }
        },
        
        'fluids': {
            'symbols': {
                'Q': {'units': 'meter**3/second', 'description': 'Flow rate'},
                'mu': {'units': 'pascal*second', 'description': 'Viscosity'},
                'Re': {'units': 'dimensionless', 'description': 'Reynolds number'},
                'delta_P': {'units': 'pascal', 'description': 'Pressure drop'},
                'f': {'units': 'dimensionless', 'description': 'Friction factor'},
                'L': {'units': 'meter', 'description': 'Pipe length'},
                'D': {'units': 'meter', 'description': 'Pipe diameter'},
            },
            'equations': {
                'flow_rate': {
                    'expression': 'Q = A * v',
                    'bidirectional': True
                },
                'reynolds': {
                    'expression': 'Re = (rho * v * D) / mu',
                    'bidirectional': True
                },
                'pipe_pressure_drop': {
                    'expression': 'delta_P = f * (L / D) * (rho * v**2 / 2)',
                    'output': 'delta_P',
                    'inputs': ['f', 'L', 'D', 'rho', 'v']
                },
                'pipe_area': {
                    'expression': 'A = pi * (D / 2)**2',
                    'output': 'A',
                    'inputs': ['D']
                },
                'friction_factor_smooth': {
                    'expression': 'f = 0.316 / Re**0.25',
                    'output': 'f',
                    'inputs': ['Re']
                }       
            }
        }
    }
}