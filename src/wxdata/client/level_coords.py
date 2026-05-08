"""
This file hosts the functions that handle the level coordinates for byte-range requests.

(C) Eric J. Drewitz 2025-2026
"""

def get_level_suffix(level_type):
    
    """
    This function returns the level type suffix.
    
    Required Arguments:
    
    1) level_type (String) - The type of level the coordinates are on.
    
    Level Types
    -----------
    
    'hybrid'
    'entire atmosphere'
    'surface':'surface',
    'boundary layer'
    'pressure'
    'mean sea level'
    'height above ground'
    'height below ground'
    'height above sea level'
    'entire atmosphere single layer'
    'low cloud layer'
    'middle cloud layer'
    'high cloud layer'
    'cloud ceiling'
    'tropopause'
    'max wind'
    'isothermal'
    'highest tropospheric freezing level'
    'sigma layer'
    'sigma level'
    'potential vorticity surface'
    'reserved'
    
    Optional Arguments: None
    
    Returns
    -------
    
    The level type suffix.    
    """
    
    level_types = {
        
        'hybrid':'hybrid level',
        'entire atmosphere':'entire atmosphere',
        'surface':'surface',
        'boundary layer':'planetary boundary layer',
        'pressure':'mb',
        'mean sea level':'mean sea level',
        'height above ground':'m above ground',
        'height below ground':'m below ground',
        'height above sea level':'m above mean sea level',
        'entire atmosphere single layer':'entire atmosphere (considered as a single layer)',
        'low cloud layer':'low cloud layer',
        'middle cloud layer':'middle cloud layer',
        'high cloud layer':'high cloud layer',
        'cloud ceiling':'cloud ceiling',
        'tropopause':'tropopause',
        'max wind':'max wind',
        'isothermal':'0C isotherm',
        'highest tropospheric freezing level':'highest tropospheric freezing level',
        'sigma layer':'sigma layer',
        'sigma level':'sigma level',
        'potential vorticity surface':'PV=2e-06 (Km^2/kg/s) surface',
        'reserved':'reserved'
    }
    
    return level_types[level_type]


def get_level_expression(levels,
                         level_type):
    
    """
    This function returns the full expression for the level.
    
    Required Arguments:
    
    1) levels (Float or Integer List) - The pressure or height levels corresponding to level type. 
        (i.e. [700, 500, 250] if level type is 'pressure' or [2, 10] if level type is 'height above ground')
    
    2) level_type (String) - The type of level the coordinates are on.
    
    Level Types
    -----------
    
    'hybrid'
    'entire atmosphere'
    'surface':'surface',
    'boundary layer'
    'pressure'
    'mean sea level'
    'height above ground'
    'height below ground'
    'height above sea level'
    'entire atmosphere single layer'
    'low cloud layer'
    'middle cloud layer'
    'high cloud layer'
    'cloud ceiling'
    'tropopause'
    'max wind'
    'isothermal'
    'highest tropospheric freezing level'
    'sigma layer'
    'sigma level'
    'potential vorticity surface'
    'reserved'
    
    Optional Arguments: None
    
    Returns
    -------
    
    The full expression for the level to make the bytes-range request.
    """
    level_type = level_type.lower()

    suffix = get_level_suffix(level_type)    
    if levels is not None:
        expression = []
        for level in levels:
            ex = f"{level} {suffix}"
            expression.append(ex)
            levels = levels
    else:
        expression = suffix
        levels = None
        
    return expression, levels
    
    
    