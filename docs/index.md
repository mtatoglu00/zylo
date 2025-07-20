# Zylo Engineering Calculator

A Python library for engineering calculations with automatic unit handling and intelligent equation solving.

## Quick Start

```python
from core.physics.mechanics import mechanics
from core.physics.conversions import ureg

# Create calculator
calc = mechanics()

# Calculate force with automatic area substitution
force = calc.force(P=100*ureg.pascal, r=0.5*ureg.meter)  # Uses A = π×r²

# Calculate pressure with direct area input
pressure = calc.force(F=100*ureg.newton, A= 0.01*ureg.meter**2)  # Direct area input

# Calculate drag force
drag = calc.drag_force(
    rho=1.225*ureg.kg/ureg.m**3,  # Air density
    C_D=0.47,                     # Drag coefficient
    r=0.1*ureg.meter,            # Radius (auto-substitutes area)
    v=20*ureg.m/ureg.s           # Velocity
)

print(f"Force: {force}")
print(f"Pressure: {pressure.to(ureg.bar)}") # Convert to bar
print(f"Drag: {drag}")
```

**Output:**

```
Force: 78.53981633974483 newton
Pressure: 0.1 bar
Drag: 3.617543940608647 newton
```

## Key Features

- **Automatic substitutions** - Provide geometric parameters, get automatic area/volume calculations
- **Unit safety** - All calculations with proper unit handling via Pint
- **Solve for any variable** - Provide n-1 parameters, solve for the nth
- **Extensible** - Easy to add new equations and substitution rules
- **Clean API** - Simple method calls with keyword arguments

## Available Calculations

### Mechanics

- `force()` - Force calculations: F = P × A
- `stress()` - Stress analysis: σ = F / A
- `drag_force()` - Drag force: F_D = ½ρC_D A v²
- `kessel_formula()` - Pressure vessel thickness

### Fluid Mechanics

- `flow_rate()` - Flow rate: Q = A × v
- `reynolds_number()` - Reynolds number: Re = ρvd/μ

### Geometry Support

Automatic substitutions for:

- Circles: A = π×r²
- Rectangles: A = l×w
- Triangles: A = ½×l×h
- Rings: A = π×(r₂² - r₁²)
- Cylinders: V = π×r²×h

## Example: Complex Substitution

```python
# Calculate drag force knowing only mass, geometry, and fluid properties
drag = calc.drag_force(
    m=50*ureg.kg,           # Mass (for density calc)
    V=40*ureg.m**3,         # Volume (ρ = m/V)
    C_D=0.47,               # Drag coefficient
    r=0.2*ureg.m,           # Radius (A = π×r²)
    v=25*ureg.m/ureg.s      # Velocity
)
# Automatically: ρ = m/V, A = π×r², then F_D = ½ρC_D A v²
```

## Materials Database

Built-in materials database with properties for common engineering materials:

```python
from core.data.materials import materials

steel = materials[0]  # S355 steel
print(f"Yield strength: {steel['yield_strength']}")
print(f"Density: {steel['density']}")
```

---

**Simple. Powerful. Extensible.**
