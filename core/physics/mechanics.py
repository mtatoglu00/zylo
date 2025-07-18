from core.math.geometry import geometry
from core.physics.conversions import conversions, ureg

class mechanics(geometry, conversions):
    """
    Provides mechanical engineering calculations.

    Inherits from:
        - geometry: Geometric calculations.
        - conversions: Unit conversions.
    """

    def __init__(self, name: str = '') -> None:
        self.name = name
        
    
    def force(self, force: float = None, pressure: float = None, area: float = None) -> float:
        """
        THIS IS LEGACY CODE AND WILL BE DEPRECATED IN THE FUTURE.
        Solve for the missing variable (force, pressure, or area) given the other two.

        Parameters:
            force (float, optional): Force in Newtons.
            pressure (float, optional): Pressure in Pascals.
            area (float, optional): Area in square meters.

        Returns:
            float: The calculated value.

        Raises:
            ValueError: If exactly two arguments are not provided.
        """
        args = [force, pressure, area]
        if args.count(None) != 1:
            raise ValueError("Provide exactly two arguments to solve for the third.")

        if force is None:
            return pressure * area
        elif pressure is None:
            return force / area
        elif area is None:
            return force / pressure

    def force_pint(self, force=None, pressure=None, area=None):
        """
        Solve for the missing variable (force, pressure, or area) given the other two.
        All arguments must be pint.Quantity with appropriate units.

        Parameters:
            force (Quantity, optional): Force (e.g., 100 * ureg.newton).
            pressure (Quantity, optional): Pressure (e.g., 200 * ureg.pascal).
            area (Quantity, optional): Area (e.g., 0.01 * ureg.meter ** 2).

        Returns:
            Quantity: The calculated value with correct units.

        Raises:
            ValueError: If exactly two arguments are not provided.
        """
        args = [force, pressure, area]
        if args.count(None) != 1:
            raise ValueError("Provide exactly two arguments to solve for the third.")

        if force is None:
            return pressure * area
        elif pressure is None:
            return force / area
        elif area is None:
            return force / pressure

    def kessel_formula(self, thickness=None, pressure=None, diameter=None, allowable_stress=None, safety_factor=None):
        """
        Solve for the missing variable in the Kessel (pressure vessel) formula using pint quantities.

        Formula (thin-walled cylinder): thickness = (pressure * diameter) / (allowable_stress / safety_factor)

        Parameters:
            thickness (Quantity, optional): Wall thickness (e.g., 10 * ureg.millimeter).
            pressure (Quantity, optional): Internal pressure (e.g., 10 * ureg.megapascal).
            diameter (Quantity, optional): Inner diameter (e.g., 10 * ureg.millimeter).
            allowable_stress (Quantity, optional): Allowable stress (e.g., 200 * ureg.megapascal).
            safety_factor (float, optional): Safety factor to apply to allowable stress.

        Returns:
            Quantity or float: The calculated value with correct units.

        Raises:
            ValueError: If not exactly one argument is missing.
        """
        args = [thickness, pressure, diameter, allowable_stress, safety_factor]
        if args.count(None) != 1:
            raise ValueError("Provide exactly four arguments to solve for the fifth.")
        
        if thickness is None:
            if allowable_stress is None or safety_factor is None:
                raise ValueError("To solve for thickness, allowable_stress and safety_factor must be provided.")
            return (pressure * diameter) / (allowable_stress / safety_factor)
        elif pressure is None:
            return (thickness * allowable_stress / safety_factor) / diameter
        elif diameter is None:
            return (thickness * allowable_stress / safety_factor) / pressure
        elif allowable_stress is None:
            return (pressure * diameter * safety_factor) / thickness
        elif safety_factor is None:
            allowable_stress = allowable_stress.to(ureg.pascal)
            pressure = pressure.to(ureg.pascal)
            thickness = thickness.to_base_units()
            diameter = diameter.to_base_units()
            sf = (thickness * allowable_stress) / (pressure * diameter)
            return sf.magnitude