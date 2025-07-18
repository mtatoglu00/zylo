import math

class geometry():
    def __init__(self):
        pass

    def area(self, length: float = None, width: float = None, 
             radius: float = None, base: float = None, height: float = None) -> float:
        """
        Calculate the area of a variaty of shapes.

        Parameters:
            length (float, optional): Length of a rectangle.
            width (float, optional): Width of a rectangle.
            radius (float, optional): Radius of a circle.
            base (float, optional): Base of a triangle.
            height (float, optional): Height of a triangle.

        Returns:
            float: Area of the calculated shape in mm<sup>2</sup>.
        
        Raises:
            ValueError: If required parameters are missing or ambiguous.
        """
        if length is not None and width is not None:
            return length * width
        elif radius is not None:
            return math.pi * radius ** 2
        elif base is not None and height is not None:
            return 0.5 * base * height
        else:
            raise ValueError("Insufficient or ambiguous parameters for area calculation.")
        
    def diameter(self, area: float) -> float:
        """
        Calculate the diameter of a circle given its area.

        Parameters:
            area (float): Area of the circle in mm<sup>2</sup>.

        Returns:
            float: Diameter of the circle in mm.
        """
        return 2 * math.sqrt(area / math.pi)