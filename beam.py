class Beam:
    def __init__(self, material=None, infill_pattern=None, infill_density=None, wall_count=None, line_width=None):
        self.material = material
        self.infill_pattern = infill_pattern
        self.infill_density = infill_density
        self.wall_count = wall_count
        self.line_width = line_width
        self.sections = []
    
    def add_section(self, section):
        # the first section added is the clamped end
        self.sections.append(section)
    
    def input_load(self, M, F, T, TF):
        self.M = M
        self.F = F
        self.T = T
        self.TF = TF

    def analysis(self):
        # first find the displacement of section by moving from free end to clamped end
        from loading import analysis
        M = self.M
        F = self.F
        T = self.T
        TF = self.TF
        analysis(M, F, T, TF, self.sections[-1])
        cumulative_length = self.sections[-1].length
        if len(self.sections) > 1:
            for i in range(len(self.sections) - 2, -1, -1):
                M = M + F * self.sections[i + 1].length
                analysis(M, F, T, TF, self.sections[i])

                #generate a reversed length to end array for later displacement calculation
                cumulative_length.append(cumulative_length[-1] + self.sections[i].length)
        else:
            pass

        cumulative_length.reverse()

        # then find displacements by moving from clamped end to free end
        self.beam_displacement = 0
        self.beam_rotation = 0
        self.beam_twist = 0
        for i in range(len(self.sections)-1):
            self.beam_displacement += self.sections[i].displacement
            self.beam_displacement += self.sections[i].rotation * (cumulative_length[i+1] if i > 0 else 0)
            self.beam_rotation += self.sections[i].rotation
            self.beam_twist += self.sections[i].twist
        self.beam_displacement += self.sections[-1].displacement
        self.beam_rotation += self.sections[-1].rotation
        self.beam_twist += self.sections[-1].twist

        # compare and find the maximum stress in the beam
        self.max_stress = 0
        self.max_stress_section = -1
        for i in range(self.sections):
            if self.sections[i].required_yield_stress > self.max_stress:
                self.max_stress = self.sections[i].required_yield_stress
                self.max_stress_section = i
        return self.beam_displacement, self.beam_rotation, self.beam_twist