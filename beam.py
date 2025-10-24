class Beam:
    def __init__(self, material=None, infill_pattern=None, infill_density=None, wall_count=None, line_width=None):
        self.material = material
        self.infill_pattern = infill_pattern
        self.infill_density = infill_density
        self.wall_count = wall_count
        self.line_width = line_width
    
    def add_section(self, section):
        self.sections.append(section)