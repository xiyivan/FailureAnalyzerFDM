def moment_load(section, applied_moment):
    b = section.width
    h = section.height
    L = section.length
    t = section.wall_thickness
    E_shell = section.E_shell
    E_core = section.E_core

    # Dimensions of the core
    b_core = b - 2 * t
    h_core = h - 2 * t

    # Moment of inertia of shell (outer rectangle minus inner core)
    I_outer = (b * h**3) / 12
    I_inner = (b_core * h_core**3) / 12
    I_shell = I_outer - I_inner

    # Composite moment of inertia using transformed section method
    n = E_core / E_shell
    I_core_transformed = n * I_inner
    I_composite = I_shell + I_core_transformed

    # End rotation (radians)
    theta = applied_moment * L / (E_shell * I_composite)

    # End displacement (meters)
    delta = applied_moment * L**2 / (2 * E_shell * I_composite)

    # Maximum stress at top surface (Pascals)
    c = h / 2
    sigma_top = applied_moment * c / I_composite # at top and bottom surface

    return (theta, delta, sigma_top)

def force_load(section, applied_force):
    # Extract parameters
    b = section.width
    h = section.height
    L = section.length
    t = section.wall_thickness
    E_shell = section.E_shell
    E_core = section.E_core

    # Dimensions of the core
    b_core = b - 2 * t
    h_core = h - 2 * t

    # Moment of inertia of shell (outer rectangle minus inner core)
    I_outer = (b * h**3) / 12
    I_inner = (b_core * h_core**3) / 12
    I_shell = I_outer - I_inner

    # Composite moment of inertia using transformed section method
    n = E_core / E_shell
    I_core_transformed = n * I_inner
    I_composite = I_shell + I_core_transformed

    # End displacement (meters)
    delta = applied_force * L**3 / (3 * E_shell * I_composite)

    # End rotation (radians)
    theta = applied_force * L**2 / (2 * E_shell * I_composite)

    # Maximum stress at top surface (Pascals)
    M = applied_force * L
    c = h / 2
    sigma_top = M * c / I_composite # at top and bottom surface

    
    # Shear stress at neutral axis
    A_shell = b * h - b_core * h_core
    A_core = b_core * h_core
    A_core_transformed = n * A_core
    A_composite = A_shell + A_core_transformed
    tau_max = (3 / 2) * applied_force / A_composite # at neutral axis


    return(delta, theta, sigma_top, tau_max)

def torsion_load(section, applied_torque):
    # Extract parameters
    b = section.width
    h = section.height
    L = section.length
    t = section.shell_thickness
    G_shell = section.G_shell
    G_core = section.G_core

    # Dimensions of the core
    b_core = b - 2 * t
    h_core = h - 2 * t

    # Polar moment of inertia approximation for rectangular section
    J_outer = (b * h**3) * (16/3) / (1.8 * b + h)
    J_inner = (b_core * h_core**3) * (16/3) / (1.8 * b_core + h_core)
    J_shell = J_outer - J_inner

    # Composite polar moment using transformed section method
    n = G_core / G_shell
    J_core_transformed = n * J_inner
    J_composite = J_shell + J_core_transformed

    # Torsional rotation (radians)
    theta = applied_torque * L / (G_shell * J_composite)

    # Maximum shear stress at outer surface
    r = max(b, h) / 2
    tau_max = applied_torque * r / J_composite # constant arround the shell

    return (theta, tau_max)

def tensile_load(section, applied_tensile_force):
    
# Extract parameters
    b = section.width
    h = section.height
    t = section.shell_thickness
    E_shell = section.E_shell
    E_core = section.E_core

    # Dimensions of the core
    b_core = b - 2 * t
    h_core = h - 2 * t

    # Areas
    A_shell = b * h - b_core * h_core
    A_core = b_core * h_core

    # Transformed core area
    n = E_core / E_shell
    A_core_transformed = n * A_core

    # Effective area
    A_eff = A_shell + A_core_transformed

    # Axial stress (same at top and bottom surfaces)
    axial_stress = applied_tensile_force / A_eff

    return axial_stress

def required_yield_stress_tresca(tensile_stress, shear_stress):
    """
    Calculate the minimum yield stress required to prevent yielding
    under combined tensile and shear stress using Tresca's criterion.

    Parameters:
    - tensile_stress: axial stress in Pascals
    - shear_stress: shear stress in Pascals

    Returns:
    - required_yield_stress: minimum yield stress in Pascals
    """
    # Principal stresses
    sigma_1 = tensile_stress / 2 + ((tensile_stress / 2)**2 + shear_stress**2)**0.5
    sigma_2 = tensile_stress / 2 - ((tensile_stress / 2)**2 + shear_stress**2)**0.5

    # Maximum shear stress
    sigma_max = abs(sigma_1 - sigma_2)

    # Required yield stress must satisfy both conditions
    required_yield_stress = max(sigma_max, sigma_1)

    return required_yield_stress 

def required_yield_stress_von_mises(tensile_stress, shear_stress):
    """
    Calculate the minimum yield stress required to prevent yielding
    under combined tensile and shear stress using Von Mises criterion.

    Parameters:
    - tensile_stress: axial stress in Pascals
    - shear_stress: shear stress in Pascals

    Returns:
    - required_yield_stress: minimum yield stress in Pascals
    """
    sigma_1 = tensile_stress / 2 + ((tensile_stress / 2)**2 + shear_stress**2)**0.5
    sigma_2 = tensile_stress / 2 - ((tensile_stress / 2)**2 + shear_stress**2)**0.5

    sigma_max = ((sigma_1**2 - (sigma_1 - sigma_2)**2 + sigma_2**2)/2)**0.5

    return sigma_max


def analysis(M, F, T, TF, section):
    if M is not None:
        theta_moment, delta_moment, sigma_moment = moment_load(section, M)
    if F is not None:
        delta_force, theta_force, sigma_force, tau_force = force_load(section, F)
    if T is not None:
        theta_torsion, tau_torsion = torsion_load(section, T)
    if TF is not None:
        axial_stress = tensile_load(section, TF)
    
    section.displacement = delta_moment + delta_force
    section.rotation = theta_moment + theta_force
    section.twist = theta_torsion

    # do mohr's circle analysis to find principal stresses

    # at the top and bottom surface
    top_surface_stress = sigma_moment + sigma_force + axial_stress
    bottom_surface_stress = -sigma_moment + -sigma_force + axial_stress
    surface_tensile_stress = max(top_surface_stress, bottom_surface_stress)
    surface_shear_stress = axial_stress

    # at the neutral axis
    neutral_axis_shear_stress = abs(tau_force) + abs(tau_torsion)
    neutral_axis_tensile_stress = axial_stress

    required_yield_stress = max(required_yield_stress_tresca(surface_tensile_stress, surface_shear_stress),
                                required_yield_stress_von_mises(surface_tensile_stress, surface_shear_stress),
                                required_yield_stress_tresca(neutral_axis_tensile_stress, neutral_axis_shear_stress),
                                required_yield_stress_von_mises(neutral_axis_tensile_stress, neutral_axis_shear_stress))
    section.required_yield_stress = required_yield_stress
    return None


