import json
import os


if __name__ == "__main__":
    from beam import Beam

    # Prompt for beam name
    beam_name = input("Please enter the name of the beam:").strip()
    if not beam_name:
        print("No beam name provided. Exiting.")
        raise SystemExit(1)

    # Ensure there's a `beams` subfolder in the current working directory
    beams_dir = os.path.join(os.getcwd(), "beams")
    os.makedirs(beams_dir, exist_ok=True)

    # We'll look for a JSON file named <beam_name>.json inside `beams`
    beam_file = os.path.join(beams_dir, f"{beam_name}.json")

    # Shared input helpers
    def ask_yes_no(prompt, default=True):
        resp = input(prompt).strip().lower()
        if resp == "":
            return default
        return resp in ("y", "yes")

    def ask_optional(prompt):
        v = input(prompt).strip()
        return v if v != "" else None

    def ask_float(prompt):
        while True:
            v = input(prompt).strip()
            try:
                return float(v)
            except Exception:
                print("Please enter a valid number.")

    # def ask_int(prompt):
    #     while True:
    #         v = input(prompt).strip()
    #         try:
    #             return int(v)
    #         except Exception:
    #             print("Please enter a valid integer.")

    def handle_existing_beam(beam_file):
        """Prompt to load an existing beam file and return (beam, loaded_flag)."""
        print(f"Beam '{beam_name}' already exists at: {beam_file}")
        choice = input("Load existing beam? [Y/n]: ").strip().lower()
        if choice in ("", "y", "yes"):
            try:
                with open(beam_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                defaults = data.get("defaults", {}) if isinstance(data, dict) else {}
                allowed_defaults = ("material", "infill_pattern", "infill_density", "wall_count", "line_width")
                beam_kwargs = {k: defaults[k] for k in allowed_defaults if k in defaults and defaults[k] is not None}
                beam = Beam(**beam_kwargs)

                for s in data.get("sections", []):
                    length = s.get("length")
                    width = s.get("width")
                    height = s.get("height")
                    if length is None or width is None or height is None:
                        continue
                    allowed_section_keys = ("material", "infill_pattern", "infill_density", "wall_count", "line_width")
                    section_kwargs = {k: s[k] for k in allowed_section_keys if k in s and s[k] is not None}
                    beam.add_section(length=length, width=width, height=height, **section_kwargs)

                print(f"Loaded beam '{beam_name}' with {len(beam.sections)} sections.")
                return beam, True
            except Exception as e:
                print(f"Failed to load existing beam file: {e}")
                print("Proceeding with a new Beam instance instead.")
                return Beam(), False
        else:
            print("Creating a new beam (existing file will remain unchanged unless you save/overwrite it).")
            return Beam(), False

    def create_new_beam_interactive(beam_file):
        """Interactively build a new beam, save it to beam_file, and return the Beam."""
        print("Let's create a new beam definition.")

        use_global = ask_yes_no("Do you want to set global properties (material, infill_pattern, infill_density, wall_count, line_width)? [Y/n]: ")
        defaults_to_save = {}
        beam = Beam()
        if use_global:
            mat = ask_optional("Material (leave blank to skip): ")
            if mat is not None:
                defaults_to_save["material"] = mat
            infill_pat = ask_optional("Infill pattern (leave blank to skip): ")
            if infill_pat is not None:
                defaults_to_save["infill_pattern"] = infill_pat
            infill_den = ask_optional("Infill density (percentage) (leave blank to skip): ")
            if infill_den is not None:
                try:
                    defaults_to_save["infill_density"] = float(infill_den)
                except Exception:
                    print("Invalid infill density, skipping.")
            wall_cnt = ask_optional("Wall count (integer) (leave blank to skip): ")
            if wall_cnt is not None:
                try:
                    defaults_to_save["wall_count"] = int(wall_cnt)
                except Exception:
                    print("Invalid wall count, skipping.")
            lw = ask_optional("Line width (mm) (leave blank to skip): ")
            if lw is not None:
                try:
                    defaults_to_save["line_width"] = float(lw)/1000
                except Exception:
                    print("Invalid line width, skipping.")

            beam_kwargs = {k: defaults_to_save[k] for k in ("material", "infill_pattern", "infill_density", "wall_count", "line_width") if k in defaults_to_save}
            beam = Beam(**beam_kwargs)

        saved_sections = []
        while True:
            add_sec = ask_yes_no("Do you want to add a new section? [Y/n]: ")
            if not add_sec:
                break

            print("Enter section geometry:")
            length = ask_float("  Length: ")
            width = ask_float("  Width: ")
            height = ask_float("  Height: ")

            section_kwargs = {}
            if not use_global:
                mat = ask_optional("  Material (leave blank to skip): ")
                if mat is not None:
                    section_kwargs["material"] = mat
                infill_pat = ask_optional("  Infill pattern (leave blank to skip): ")
                if infill_pat is not None:
                    section_kwargs["infill_pattern"] = infill_pat
                infill_den = ask_optional("  Infill density (leave blank to skip): ")
                if infill_den is not None:
                    try:
                        section_kwargs["infill_density"] = float(infill_den)
                    except Exception:
                        print("  Invalid infill density, skipping.")
                wall_cnt = ask_optional("  Wall count (leave blank to skip): ")
                if wall_cnt is not None:
                    try:
                        section_kwargs["wall_count"] = int(wall_cnt)
                    except Exception:
                        print("  Invalid wall count, skipping.")
                lw = ask_optional("  Line width (mm) (leave blank to skip): ")
                if lw is not None:
                    try:
                        section_kwargs["line_width"] = float(lw)/1000
                    except Exception:
                        print("  Invalid line width, skipping.")

            beam.add_section(length=length, width=width, height=height, **section_kwargs)

            sec_to_save = {"length": length, "width": width, "height": height}
            for k, v in section_kwargs.items():
                sec_to_save[k] = v
            saved_sections.append(sec_to_save)

        data_to_save = {}
        if defaults_to_save:
            data_to_save["defaults"] = defaults_to_save
        data_to_save["sections"] = saved_sections

        try:
            with open(beam_file, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=2)
            print(f"Saved new beam to: {beam_file}")
        except Exception as e:
            print(f"Failed to save beam file: {e}")

        return beam

    # Main flow: either handle existing file or create a new beam interactively
    if os.path.exists(beam_file):
        beam, loaded = handle_existing_beam(beam_file)
        if not loaded:
            beam = create_new_beam_interactive(beam_file)
    else:
        beam = create_new_beam_interactive(beam_file)

    # Placeholder: continue with program flow (e.g., prompt user to set loads, run analysis...)
    print("You can now set loads, run analysis, or edit/save the beam later.")

    # Ask user whether to run analysis now
    if ask_yes_no("Do you want to run analysis now? [Y/n]: "):
        print("Enter load values (numeric). Leave blank to use 0.")

        def ask_float_allow_blank(prompt, default=0.0):
            v = input(prompt).strip()
            if v == "":
                return float(default)
            try:
                return float(v)
            except Exception:
                print("Invalid number, using 0.")
                return float(default)

        M = ask_float_allow_blank("  Moment M: ")
        F = ask_float_allow_blank("  Transverse force F: ")
        T = ask_float_allow_blank("  Torsion T: ")
        TF = ask_float_allow_blank("  Tensile force TF: ")

        # Provide loads to beam and run analysis
        # try:
        beam.input_load(M, F, T, TF)
        result = beam.analysis()
        if result is None:
            # Some analysis implementations may set attributes instead of returning
            disp = getattr(beam, "beam_displacement", None)
            rot = getattr(beam, "beam_rotation", None)
            twist = getattr(beam, "beam_twist", None)
        else:
            disp, rot, twist = result

        print("Analysis results:")
        print(f"  Displacement: {disp}")
        print(f"  Rotation: {rot}")
        print(f"  Twist: {twist}")
        # except Exception as e:
        #     print(f"Analysis failed: {e}")