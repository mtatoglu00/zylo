from core.math.geometry import geometry
from core.physics.mechanics import mechanics
from core.physics.conversions import conversions, ureg

if __name__ == '__main__':

    materials = [
        {"name": "S355", 
         "yield_strength": 355e6 * ureg.pascal, 
         "density": 7850 * ureg.kilogram / ureg.meter ** 3, 
         "young_modulus": 210e9 * ureg.pascal}
        ]

    test = mechanics()

    force = 150 #kN
    pressure = 200 #bar
    hub = 500 #mm

    inner_diameter = test.diameter(test.force(force=test.convert_force(force, 'kN', 'N'),
                                    pressure=test.convert_pressure(pressure, 'bar', 'Pa')))
    
    print(test.convert_metric(inner_diameter, 'm', 'mm'), 'mm')

    f = 150 * ureg.kilonewton
    p = 200 * ureg.bar
    hub = 500 * ureg.millimeter

    fpint = test.force_pint(force=f, pressure=p)

    diameter = 2 * (fpint / ureg.pi) ** 0.5
    diameter = diameter.to(ureg.millimeter)
    print(f"Diameter: {diameter:~P}")
    
    #print(list(ureg))
    print(ureg.get_compatible_units('newton'))
################################################################################

    m = mechanics()
    pressure = 200 * ureg.bar
    radius =  diameter
    allowable_stress = materials[0]["yield_strength"]
    safety_factor = 2.0

    thickness = m.kessel_formula(
        pressure=pressure,
        diameter=diameter,
        allowable_stress=allowable_stress,
        safety_factor=safety_factor
    )

    print(f"Required wall thickness: {thickness.to(ureg.millimeter):.2f~P}")

################################################################################

    print(f"The safety is: {m.kessel_formula(
        thickness= thickness,
        pressure=pressure,
        diameter=diameter,
        allowable_stress=allowable_stress,
    ):.2f}")
    


test2 = mechanics()

print(test2.name)

n = test2.area(base=10, height=5)
print(n)
test2.diameter

print(test2.force(pressure=10000, area=1))
print(test2.force(pressure=10000, force=10000))