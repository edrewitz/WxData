"""
This file hosts functions that are common exception errors for the GDPS Download

(C) Eric J. Drewitz 2025-2026
"""

def invalid_info(has_levels):
    
    """
    Returns an error for invalid information.
    
    Required Arguments:
    
    1) has_levels (Boolean) - If True, the variable is found at multiple levels.
        
    Optional Arguments: None
    
    Returns
    -------
    
    An error message and instructions on how to fix the error for invalid user input. 
    """
        
    print("Error: User Entered Invalid Information.")
    
    if has_levels == True:
    
        print(f"""
            Consider the following:
            
            1) Try double checking the spelling of your variable.
            
            2) Try checking to make sure your levels are correct.
            
                Here is how to format the correct levels
                ----------------------------------------
                
                if type_of_level='pressure' => level=pressure level (level=500 = example for 500mb)
                if type_of_level='height above ground' => level=height above ground level (level=10 = example for 10m)
                if type_of_level='pressure layer' => layer=[pressure at lower level, pressure at higher level] (layer=[1000, 500] = example for 1000mb to 500mb)
                if type_of_level='depth below surface' => layer=[height of higher level, height at lower level] (layer=[0, 10] = example for 0cm to 10cm)
                if type_of_level='potential vorticity surface' => level=potential vorticity surface (level=1.5 = example for 1.5 PVU)
                
                Some parameters such as 'absolute vorticity' are not found at all the same levels as other parameters such as 'air temperature'
                In these cases, the best practice is to download different datasets each with levels that are consistent between parameters.
                
                
            3) Try double checking the level corresponds correctly to the parameter. Please check at: https://dd.weather.gc.ca/
            
            Visit: https://github.com/edrewitz/WxData/wiki#canadian-meteorological-centre to view the documentation.
            """)
        
    else:
        print("Consider the following:")
        print("Try double checking the spelling of your variable.")
        print("Try double checking to make sure your level_type is correct.")