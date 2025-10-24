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
    
    