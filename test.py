from core.physics.mechanics import mechanics
from core.physics.conversions import ureg

# Create calculator - everything auto-configured
calc = mechanics("My Engineering Calculator")

# Test calculations
force = calc.force(P=100*ureg.pascal, r=0.5*ureg.meter)
drag = calc.drag_force(rho=1.225*ureg.kg/ureg.m**3, C_D=0.47, l=2*ureg.meter, w=1*ureg.meter, v=20*ureg.m/ureg.s)
area = calc.solve('circle_area', r=0.5*ureg.meter)
volume = calc.solve('cylinder_volume', r=0.1*ureg.meter, h=2*ureg.meter)
flow = calc.flow_rate(A=0.1*ureg.meter**2, v=5*ureg.meter/ureg.second)
reynolds = calc.reynolds_number(rho=1000*ureg.kg/ureg.m**3, v=2*ureg.m/ureg.s, D=0.1*ureg.m, mu=0.001*ureg.pascal*ureg.second)


print(f"Force: {force}")
print(f"Drag: {drag}")
print(f"Area: {area}")
print(f"Volume: {volume}")
print(f"Flow Rate: {flow}")
print(f"Reynolds Number: {reynolds}")

# More advanced calculations
force = calc.force(P=100*ureg.bar, A=500000*ureg.millimeter**2)  # Direct area input
print(f"High Pressure Force: {force}")

force = calc.force(P=100000*ureg.mbar, A=0.5*ureg.meter**2)  # Direct area input
print(f"Calculated Force: {force}")

drag = calc.drag_force(
    rho=1.225*ureg.kg/ureg.m**3, 
    F_D=230*ureg.newton, 
    l=2*ureg.meter, 
    w=1*ureg.meter, 
    v=20*ureg.m/ureg.s)

print(f"Calculated Drag Force: {drag}")

c_d = calc.solve('drag', rho=1.225*ureg.kg/ureg.m**3, 
                F_D=230*ureg.newton, 
                l=2*ureg.meter, 
                w=1*ureg.meter, 
                v=20*ureg.m/ureg.s)

print(f"Calculated Drag Coefficient: {c_d}")

area = calc.solve('circle_area', r=0.5*ureg.meter)
print(f"Calculated Circle Area: {area}")

diameter = calc.solve('circle_area', A=area)
print(f"Calculated Diameter: {diameter}")


# Example 1: Calculate pressure drop (lots of substitutions!)
pressure_drop = calc.solve('pipe_pressure_drop',
    Q=0.1*ureg.meter**3/ureg.second,        # Flow rate → v (via A)
    D=0.2*ureg.meter,                       # Diameter → A, Re
    L=100*ureg.meter,                       # Pipe length
    rho=1000*ureg.kg/ureg.meter**3,         # Density → Re
    mu=0.001*ureg.pascal*ureg.second)       # Viscosity → Re → f

print(f"Pipe Pressure Drop: {pressure_drop}")