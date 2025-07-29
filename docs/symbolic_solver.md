# Symbolic Solver

The heart of Zylo's intelligent equation solving system. Provides automatic substitutions and flexible equation solving without domain-specific knowledge.

## Core Concept

The `SymbolicSolver` is a general-purpose equation solver that:

1. **Manages symbols** with units and properties
2. **Stores equations** as symbolic expressions
3. **Applies substitution rules** automatically
4. **Solves for any variable** given n-1 parameters

## Architecture

```
SymbolicSolver (general)
├── Symbols + Units
├── Equations
├── Substitution Rules
└── Smart Solving Logic

Domain-Specific Files:
├── rules/geometry_rules.py     → Geometric substitutions
├── equations/mechanics_equations.py → Mechanical equations
└── physics/mechanics.py       → Simple wrapper methods
```

## How It Works

### 1. Symbol Management

```python
# Symbols are defined with units and properties
geometric_symbols = {
    'r': {'units': ureg.meter, 'properties': {'real': True, 'positive': True}},
    'A': {'units': ureg.meter**2, 'properties': {'real': True, 'positive': True}},
}
solver.add_symbols(geometric_symbols)
```

### 2. Substitution Rules

```python
# Rules define how to calculate one symbol from others
solver.add_substitution_rule('A', ['r'], sp.pi * solver.symbols['r']**2)
# Meaning: A can be calculated from r using A = π×r²
```

### 3. Equations

```python
# Equations are stored as symbolic expressions
F, P, A = solver.symbols['F'], solver.symbols['P'], solver.symbols['A']
solver.add_equation('force', sp.Eq(F, P * A))
# Stores: F = P × A
```

### 4. Smart Solving

```python
# Automatically finds substitutions and solves
force = solver.solve_smart('force', ['F', 'P', 'A'], P=100*ureg.pascal, r=0.5*ureg.meter)
# Process: r → A = π×r² → F = P×A → solve for F
```

## Adding New Equations

### Step 1: Create Equation File

```python
# equations/new_domain_equations.py
import sympy as sp
from core.physics.conversions import ureg

def setup_new_equations(solver):
    """Add new domain equations."""

    # Add symbols
    symbols = {
        'E': {'units': ureg.joule, 'properties': {'real': True, 'positive': True}},  # Energy
        'm': {'units': ureg.kilogram, 'properties': {'real': True, 'positive': True}},  # Mass
        'c': {'units': ureg.meter/ureg.second, 'properties': {'real': True, 'positive': True}},  # Speed
    }
    solver.add_symbols(symbols)

    # Get symbols for equation creation
    E, m, c = solver.symbols['E'], solver.symbols['m'], solver.symbols['c']

    # Add equations
    E, m, c = solver.symbols['E'], solver.symbols['m'], solver.symbols['c']
    solver.add_equation('energy_mass', sp.Eq(E, m * c**2))  # E = mc²
```

### Step 2: Add Substitution Rules (Optional)

```python
# rules/new_domain_rules.py
def setup_new_rules(solver):
    """Add domain-specific substitution rules."""

    # Example: kinetic energy substitution
    solver.add_substitution_rule('E', ['m', 'v'], 0.5 * solver.symbols['m'] * solver.symbols['v']**2)
```

### Step 3: Create Wrapper Methods

```python
# physics/new_domain.py
from core.math.symbolic_solver import SymbolicSolver
from core.equations.new_domain_equations import setup_new_equations

class new_domain:
    def __init__(self):
        self.solver = SymbolicSolver()
        setup_new_equations(self.solver)

    def energy(self, **kwargs):
        """Calculate energy: E = mc²"""
        return self.solver.solve_smart('energy_mass', ['E', 'm', 'c'], **kwargs)
```

### Step 4: Use It

```python
calc = new_domain()
energy = calc.energy(m=1*ureg.kg, c=299792458*ureg.m/ureg.s)
# Returns: 8.987551787368176e+16 joule
```

## Key Features

### Automatic Substitution Detection

```python
# The solver automatically finds substitution chains:
drag = calc.drag_force(
    m=50*ureg.kg,           # Mass
    V=40*ureg.m**3,         # Volume
    C_D=0.47,               # Drag coefficient
    r=0.2*ureg.m,           # Radius
    v=25*ureg.m/ureg.s      # Velocity
)

# Automatic substitution chain:
# 1. ρ = m/V (density from mass/volume)
# 2. A = π×r² (area from radius)
# 3. F_D = ½ρC_D A v² (drag force)
```

### Unit Safety

- All calculations preserve units automatically
- Conversion between compatible units handled seamlessly
- Unit mismatch errors caught early

### Flexible Solving

```python
# Solve for any variable by providing the others:
force = calc.force(P=100*ureg.pascal, A=0.5*ureg.m**2)        # F = P×A
pressure = calc.force(F=100*ureg.newton, A=0.5*ureg.m**2)     # P = F/A
area = calc.force(F=100*ureg.newton, P=200*ureg.pascal)       # A = F/P
```

## Best Practices

1. **Keep SymbolicSolver general** - No domain knowledge in the core solver keep everything clean!
2. **Separate concerns** - Rules in `/rules/`, equations in `/equations/`, wrappers in `/physics/`
3. **Consistent naming** - Use standard engineering symbols (F, P, A, etc.)
4. **Document units** - Always specify units in symbol definitions
5. **Test substitutions** - Verify complex substitution chains work correctly

## Error Handling

The solver provides clear error messages:

```python
# Missing parameters
ValueError: Cannot solve. Missing: ['F', 'A'], Available subs: []

# Too many parameters
ValueError: Cannot solve. Missing: [], Available subs: ['A']
```
