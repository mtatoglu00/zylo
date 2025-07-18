import pint

ureg = pint.UnitRegistry()

class conversions():
    """
    THIS IS LEGACY CODE AND WILL BE DEPRECATED IN THE FUTURE.
    Provides unit conversion methods for now.
    Later on this will be changed/replaced by pint or astropy units.
    """
    def __init__(self):
        pass

    def convert_metric(self, value, from_unit, to_unit, power=1):
        """
        Convert between metric units for length, area, and volume.

        Parameters:
            value (float): The value to convert.
            from_unit (str): The unit to convert from (e.g., 'mm', 'cm', 'm', 'km', 'um').
            to_unit (str): The unit to convert to (e.g., 'mm', 'cm', 'm', 'km', 'um').
            power (int): The power for conversion (1=length, 2=area, 3=volume).

        Returns:
            float: Converted value.

        Raises:
            ValueError: If units are not recognized.
        """
        units = {
            'um': 1e-6,
            'mm': 1e-3,
            'cm': 1e-2,
            'm': 1,
            'km': 1e3
        }
        if from_unit not in units or to_unit not in units:
            raise ValueError("Unknown units.")
        factor = (units[from_unit] / units[to_unit]) ** power
        return value * factor
    
    def convert_force(self, value, from_unit, to_unit):
        """
        Convert between metric force units.

        Parameters:
            value (float): The value to convert.
            from_unit (str): The unit to convert from ('mN', 'N', 'kN', 'MN').
            to_unit (str): The unit to convert to ('mN', 'N', 'kN', 'MN').

        Returns:
            float: Converted value.

        Raises:
            ValueError: If units are not recognized.
        """
        units = {
            'mN': 1e-3,
            'N': 1,
            'kN': 1e3,
            'MN': 1e6
        }
        if from_unit not in units or to_unit not in units:
            raise ValueError("Unknown force units.")
        factor = units[from_unit] / units[to_unit]
        return value * factor

    def convert_pressure(self, value, from_unit, to_unit):
        """
        Convert between metric pressure units.

        Parameters:
            value (float): The value to convert.
            from_unit (str): The unit to convert from ('mPa', 'Pa', 'kPa', 'MPa', 'GPa', 'mbar', 'bar').
            to_unit (str): The unit to convert to ('mPa', 'Pa', 'kPa', 'MPa', 'GPa', 'mbar', 'bar').

        Returns:
            float: Converted value.

        Raises:
            ValueError: If units are not recognized.
        """
        units = {
            'mPa': 1e-3,
            'Pa': 1,
            'kPa': 1e3,
            'MPa': 1e6,
            'GPa': 1e9,
            'mbar': 1e2,
            'bar': 1e5
        }
        if from_unit not in units or to_unit not in units:
            raise ValueError("Unknown pressure units.")
        factor = units[from_unit] / units[to_unit]
        return value * factor

test = conversions()
# print(test.convert_metric(1.875, 'm', 'mm', 2))
# print(test.convert_force(1000, 'N', 'kN'))
# print(test.convert_force(2, 'mN', 'N'))
# print(test.convert_pressure(1, 'MPa', 'Pa'))
# print(test.convert_pressure(1, 'bar', 'Pa'))

#value = test.convert_metric(1250, 'mm', 'm')

#print(value)