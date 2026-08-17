"""
This file hosts the function that builds the HGEFS Directory

(C) Eric J. Drewitz 2025-2026
"""

import os


def build_directory(type_of_level,
                    cat):
    
    """
    This function builds the HGEFS directory
    
    Required Arguments: 
    
    1) type_of_level (String) - Default='pressure'. The type of level the data is in.
    
        Types of Levels
        ---------------
        
        1) pressure
        2) surface
        
    2) cat (String) - Default='mean'. The category of the data.
    
        Catagories
        ----------
        
        1) mean
        2) spread
        
    Returns
    -------
    
    A directory for the HGEFS Data    
    """
    
    try:
        os.makedirs(f"HGEFS/{type_of_level.upper()}/{cat.upper()}")
    except Exception as e:
        pass
    
    path = f"HGEFS/{type_of_level.upper()}/{cat.upper()}"
    
    return path