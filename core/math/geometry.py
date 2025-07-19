import math
from core.physics.conversions import ureg

class geometry():
    """Lightweight geometry class for direct calculations when you don't need the full equation system."""
    
    def area(self, length=None, width=None, radius=None, **kwargs):
        """Simple direct area calculations."""
        if radius is not None:
            return math.pi * radius ** 2
        elif length is not None and width is not None:
            return length * width
        elif length is not None and kwargs.get('height') is not None:
            return 0.5 * length * kwargs['height']  # Triangle
        else:
            raise ValueError("Insufficient parameters for area calculation.")
    
    def diameter(self, area=None, radius=None):
        """Calculate diameter from area or radius."""
        if area is not None:
            return 2 * math.sqrt(area / math.pi)
        elif radius is not None:
            return 2 * radius
        else:
            raise ValueError("Provide either area or radius.")

