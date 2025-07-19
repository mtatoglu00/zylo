from core.math.geometry import geometry
from core.physics.mechanics_old import mechanics as mechanics_old
from core.physics.mechanics import mechanics
from core.physics.conversions import conversions, ureg

if __name__ == '__main__':

    materials = [
        {"name": "S355", 
         "yield_strength": 355e6 * ureg.pascal, 
         "density": 7850 * ureg.kilogram / ureg.meter ** 3, 
         "young_modulus": 210e9 * ureg.pascal}
        ]
    
    f = 150 * ureg.kilonewton
    p = 200 * ureg.bar
    hub = 500 * ureg.millimeter


    from sympy import symbols, Eq, solve

    F, p, A = symbols('F p A')
    eq = Eq(F, p * A)
    solution = solve(eq.subs({F: 21428, A: 12}), p)
    print(solution)

################################################################################

    # Example usage of new mechanics class with pint quantities and substitutions
    calc = mechanics("My Engineering Calculator")

 # All of these work automatically:
    force1 = calc.force(P=100*ureg.pascal, r=0.5*ureg.meter)     # A = π*r²
    force2 = calc.force(P=100*ureg.pascal, d=1.0*ureg.meter)     # A = π*(d/2)²
    force3 = calc.force(P=100*ureg.pascal, l=2*ureg.meter, w=1*ureg.meter)  # A = l*w

    print(f"Calculated Force: {force1}")
    print(f"Calculated Force with diameter: {force2}")
    print(f"Calculated Stress: {force3}")

################################################################################

    # Test drag equation with geometry substitutions
    print("\n=== Drag Force Calculations ===")
    
    # Test 1: Drag force for a circular object (using radius)
    drag_force_circle = calc.drag_force(
        rho=1.225 * ureg.kilogram / ureg.meter**3,  # Air density at sea level
        C_D=0.47,  # Drag coefficient for sphere
        r=0.1 * ureg.meter,  # 10cm radius sphere
        v=20 * ureg.meter / ureg.second  # 20 m/s velocity
    )
    print(f"Drag force (sphere, r=0.1m): {drag_force_circle}")
    
    # Test 2: Drag force for a rectangular object (using length and width)
    drag_force_rect = calc.drag_force(
        rho=1.225 * ureg.kilogram / ureg.meter**3,
        C_D=1.05,  # Drag coefficient for flat plate
        l=2.0 * ureg.meter,  # 2m length
        w=1.0 * ureg.meter,  # 1m width
        v=15 * ureg.meter / ureg.second
    )
    print(f"Drag force (rectangle, 2m×1m): {drag_force_rect}")
    
    # Test 3: Solve for velocity given drag force and circular area
    velocity = calc.drag_force(
        F_D=100 * ureg.newton,  # Known drag force
        rho=1.225 * ureg.kilogram / ureg.meter**3,
        C_D=0.47,
        r=0.15 * ureg.meter  # 15cm radius
    )
    print(f"Required velocity for 100N drag: {velocity}")
    
    # Test 4: Solve for drag coefficient
    drag_coeff = calc.drag_force(
        F_D=50 * ureg.newton,
        rho=1.225 * ureg.kilogram / ureg.meter**3,
        A=0.5 * ureg.meter**2,  # Direct area input
        v=10 * ureg.meter / ureg.second
    )
    print(f"Drag coefficient: {drag_coeff}")


################################################################################
    # Testing auto substitution and solving for different parameters
    print("\n=== Mechanics Calculations ===")

    # Force calculations
    force = calc.force(P=100*ureg.pascal, r=0.5*ureg.meter)     # Substitutes A = π*r²
    force = calc.force(P=100*ureg.pascal, l=2*ureg.meter, w=1*ureg.meter)  # Substitutes A = l*w

    # Drag calculations  
    drag = calc.drag_force(rho=1.225*ureg.kg/ureg.m**3, C_D=0.47, r=0.1*ureg.m, v=20*ureg.m/ureg.s)

    # Stress calculations
    stress = calc.stress(F=1000*ureg.newton, r=0.05*ureg.meter)  # Substitutes A = π*r²

    # Solve for any variable
    velocity = calc.drag_force(F_D=100*ureg.newton, rho=1.225*ureg.kg/ureg.m**3, C_D=0.47, r=0.15*ureg.m)

    force2 = calc.force(P=100*ureg.bar, A=0.01*ureg.meter**2)

    print(f"Calculated Force: {force2}")

    print(f"Calculated Force: {force}"
          f"\nCalculated Drag Force: {drag}"
          f"\nCalculated Stress: {stress}"
          f"\nCalculated Velocity: {velocity}")

    
    flow = calc.flow_rate(A=0.1*ureg.meter**2, v=5*ureg.meter/ureg.second)
    reynolds = calc.reynolds_number(rho=1000*ureg.kg/ureg.m**3, v=2*ureg.m/ureg.s, 
                                    d=0.1*ureg.m, mu=0.001*ureg.pascal*ureg.second)
    
    print(f"Flow Rate: {flow}"
            f"\nReynolds Number: {reynolds}")

    # Debugging

    # Check what symbols are available
    #print("Available symbols:", list(calc.solver.symbols.keys()))

    # Check what equations are loaded
    #print("Available equations:", list(calc.solver.equations.keys()))

    # Check substitution rules
    #print("Substitution rules:", calc.solver.substitution_rules)