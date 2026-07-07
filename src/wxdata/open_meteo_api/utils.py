"""
This file has helper functions to assist with extracting and parsing data from the Open-Meteo API

(C) Eric J. Drewitz 2025-2026
"""

import pandas as _pd
import sys as _sys

def server_response(response):
    
    """
    Checks to see if the server response status code is 200 and if response status code != 200 return an error.
    
    Required Arguments: 
    
    1) response (http object)
    
    Optional Arguments: None
    
    Returns
    -------
    
    An error message if response status code != 200    
    """
    
    if response.status_code == 200:
        pass
    else:
        print("Error: https://open-meteo.com/ is down.\nPlease try again later.")
        _sys.exit(1)


def _flatten_json_arrays(data, 
                        parent_key='', 
                        sep='_'):
    """
    This function flattens the json arrays to allow Pandas.DataFrames to be created.
    
    Required Arguments:
    
    data (JSON) - The data in the form of a json object. 
    
    Optional Arguments:
    
    1) parent_key (String) - (Default=''). 
    
    2) sep (String) - (Default='_').
    
    Returns
    -------
    
    
    """
    items = {}
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            # Recursively flatten nested dictionaries
            items.update(_flatten_json_arrays(v, new_key, sep=sep))
        elif isinstance(v, list):
            # Capture the array/record path automatically
            items[new_key] = v
        else:
            # Capture top-level scalar values if needed
            items[new_key] = [v]
            
    return items

def json_to_pandas(data):
    
    """
    This function creates a Pandas.DataFrame from a flattened JSON object.
    
    Required Arguments:
    
    1) data (JSON) - The flattened JSON object.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A Pandas.DataFrame of the data retrieved from the Open-Meteo API.     
    """
    
    flattened_data = _flatten_json_arrays(data['hourly'])
    df = _pd.DataFrame(flattened_data)
    
    return df