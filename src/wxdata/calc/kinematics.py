"""
This file hosts functions that perform calculations using kinematics equations

(C) Eric J. Drewitz 2025
"""
import numpy as np

def get_u_and_v(wind_speed, 
                wind_dir):

    """
    This function calculates the u and u wind components

    Required Arguments:

    1) wind_speed (Float or Integer) 

    2) wind_direction (Float or Integer)

    Returns
    -------

    u and v wind components
    """
    
    radians = np.deg2rad(wind_dir)

    u = -wind_speed * np.sin(radians)
    v = -wind_speed * np.cos(radians)

    return u, v
