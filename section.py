import json
class Section:
    def __init__(self, length, width, height, beam=None, material=None, infill_pattern=None, infill_density=None, wall_count=None, line_width=None):
        self.length = length
        self.width = width
        self.height = height
        if beam is not None:
            self.material = beam.material
            self.infill_pattern = beam.infill_pattern
            self.infill_density = beam.infill_density
            self.wall_count = beam.wall_count
            self.line_width = beam.line_width
        else:
            self.material = beam.material
            self.infill_pattern = beam.infill_pattern
            self.infill_density = beam.infill_density
            self.wall_count = beam.wall_count
            self.line_width = beam.line_width
        
        self.wall_thickness = self.wall_count * self.line_width
        self.load_material_properties()
    
    def load_material_properties(self, material_database = "materials.json"):

        with open(material_database, 'r') as f:
            materials = json.load(f)
        
        if self.material in materials:
            mat_props = materials[self.material]
            self.E_shell = mat_props['modulus_of_elasticity']  # Pascals
            self.G_shell = mat_props['shear_modulus']  # Pascals
            self.tensile_strength = mat_props['tensile_strength']  # Pascals
        else:
            raise ValueError(f"Material '{self.material}' not found in database.")

    def set_local_load_conditions(self, M=0, F=0, T=0, TF=0):
        self.M = M  # Applied moment
        self.F = F  # Applied force
        self.T = T  # Applied torque
        self.TF = TF  # Applied tensile force

