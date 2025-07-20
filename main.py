from core.physics.mechanics import mechanics
from core.physics.conversions import ureg
from core.data.materials_db import MATERIALS_DB

from core.workflow.hydraulic_cylinder_workflow import HydraulicCylinderWorkflow

if __name__ == '__main__':

    S355 = MATERIALS_DB['S355']
    print(f"S355 Yield Strength: {S355['yield_strength']}")

    print(S355['yield_strength'].to(ureg.megapascal))
    
    p = 200 * ureg.bar
    b = 0.3 * ureg.meter
    h = 0.5 * ureg.meter
    hub = 500 * ureg.millimeter
    volume = hub * b * h

    mass = S355['density']*volume

    calc = mechanics("My Engineering Calculator")

    print((mass * 9.81*ureg.meter/ureg.second**2).to(ureg.newton))

    deflection = calc.solve('beam_deflection', 
               F= mass * 9.81*ureg.meter/ureg.second**2,
               L=hub, 
               E=S355['yield_strength'], 
               b=b, 
               h=h)

    print(f"Beam deflection: {deflection}")
    print(f"Volume:  {volume}")
    
    # Debugging

    # Check what symbols are available
    #print("Available symbols:", list(calc.solver.symbols.keys()))

    # Check what equations are loaded
    #print("Available equations:", list(calc.solver.equations.keys()))

    # Check substitution rules
    #print("Substitution rules:", calc.solver.substitution_rules)


    
    # Example inputs
    required_force = 1000 * ureg.kilonewton
    operating_pressure = 300 * ureg.bar
    stroke_length = 1.0 * ureg.meter
    material_name = 'S355'
    safety_factor = 2.0

    workflow = HydraulicCylinderWorkflow(
        force=required_force,
        pressure=operating_pressure,
        stroke=stroke_length,
        material_name=material_name,
        safety_factor=safety_factor
    )
    results = workflow.run()
    print("Hydraulic Cylinder Sizing Results:")  
    for k, v in results.items():
        print(f"{k}: {v}")
    