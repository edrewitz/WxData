"""
This file hosts the function that determines the QC-Test type from MADIS.

(C) Eric J. Drewitz 2025-2026
"""
import sys

def qc_level(qc_level):
    
    """
    This function determines the QC test type for our HTTP request.
    
    Required Arguments:
    
    1) qc_level (String) - The amount of quality control checks for a dataset.
    
    ***QC Levels***
    
    'return all observations regardless of quality control results'
    'return observations passing level 1'
    'return observations passing levels 1 and 2'
    'return observations passing levels 1 through 3'
    'return observations passing all quality control checks'
    """
    
    qc_levels = {
        
        'return all observations regardless of quality control results':'0',
        'return observations passing level 1':'1',
        'return observations passing levels 1 and 2':'2',
        'return observations passing levels 1 through 3':'3',
        'return observations passing all quality control checks':'99'
    }
    
    try:
        return qc_levels[qc_level]
    except Exception as e:
        print(f"{qc_level} is not a valid QC Level.")
        print(f"""
              
              **Valid QC Levels**
              
            'return all observations regardless of quality control results'
            
            'return observations passing level 1'
            
            'return observations passing levels 1 and 2'
            
            'return observations passing levels 1 through 3'
            
            'return observations passing all quality control checks'
              
              """)
        
        print("Please try again...\nSystem Exit.")
        sys.exit(1)