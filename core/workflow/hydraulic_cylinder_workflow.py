from core.physics.mechanics import mechanics
from core.physics.conversions import ureg
from core.data.materials_db import MATERIALS_DB
import math

class HydraulicCylinderWorkflow:
    """
    Hydraulic cylinder sizing workflow.

    This workflow calculates the required bore diameter, wall thickness, and mass of a hydraulic cylinder pipe
    based on the desired force, operating pressure, stroke length, material, and safety factor.

    Approach:
    - Calculates piston area from force and pressure.
    - Determines bore diameter from area.
    - Calculates minimum wall thickness using the thin-walled cylinder formula:
    s_min = (p * d) / (2 * sigma_allow)
    where p is pressure (N/mm²), d is bore diameter (mm), and sigma_allow is allowable stress (N/mm²).
    - Uses symbolic solver and equation database for geometry calculations.
    - Returns all relevant dimensions and mass.

    Note:
    - The equation for wall thickness in the equation database should include the factor of 2 in the denominator.
    - Symbols should use consistent units (mm, N/mm²) for this calculation.
    - For thick-walled cylinders, a more advanced formula may be needed.
    """
    def __init__(self, force, pressure, stroke, material_name, safety_factor=1.5):
        self.force = force.to(ureg.newton)
        self.pressure = pressure.to(ureg.pascal)
        self.stroke = stroke.to(ureg.meter)
        self.material = MATERIALS_DB[material_name]
        self.safety_factor = safety_factor
        self.calc = mechanics("Cylinder Workflow")

    def run(self):
        # Calculate wall thickness directly - let auto-substitution handle everything
        p_Nmm2 = self.pressure.to(ureg.newton / ureg.millimeter**2)
        
        # Single solve call handles the entire chain automatically
        wall_thickness_mm = self.calc.solve(
            'kessel',
            P=p_Nmm2,
            F=self.force,
            yield_strength=self.material['yield_strength'],
            safety_factor=self.safety_factor
        ).to(ureg.millimeter)
        
        # Calculate other needed values using the solver too
        area = self.calc.solve('force', F=self.force, P=self.pressure).to(ureg.meter**2)
        bore_diameter_m = self.calc.solve('circle_area', A=area).to(ureg.meter) * 2  # diameter = 2*radius
        bore_diameter_mm = bore_diameter_m.to(ureg.millimeter)

        # Rest of calculations stay the same...
        outer_diameter_mm = bore_diameter_mm + 2 * wall_thickness_mm
        r_outer_m = (outer_diameter_mm / 2).to(ureg.meter)
        r_inner_m = (bore_diameter_mm / 2).to(ureg.meter)
        wall_volume = (math.pi * self.stroke * (r_outer_m**2 - r_inner_m**2)).to(ureg.meter**3)
        wall_mass = (self.material['density'] * wall_volume).to(ureg.kilogram)

        return {
            'bore_diameter': bore_diameter_mm,
            'wall_thickness': wall_thickness_mm,
            'outer_diameter': outer_diameter_mm,
            'pipe_wall_mass': wall_mass.to(ureg.kilogram),
            'bottom_thickness': wall_thickness_mm*3
        }