import json
class Section:
    def __init__(self, length, width, height, material=None, infill_pattern=None, infill_density=None, wall_count=None, line_width=None):
        self.length = length
        self.width = width
        self.height = height

        self.material = material
        self.infill_pattern = infill_pattern
        self.infill_density = infill_density
        self.wall_count = wall_count
        self.line_width = line_width
        
        self.wall_thickness = self.wall_count * self.line_width
        self.load_material_properties()
    
    def load_material_properties(self, material_database = "materials.json"):

        with open(material_database, 'r') as f:
            materials = json.load(f)
        
        if self.material in materials:
            mat_props = materials[self.material]
            self.E_shell = mat_props['youngs_modulus']  # Pascals
            self.G_shell = mat_props['shear_modulus']  # Pascals
            self.tensile_strength = mat_props['tensile_strength']  # Pascals
        else:
            raise ValueError(f"Material '{self.material}' not found in database.")

