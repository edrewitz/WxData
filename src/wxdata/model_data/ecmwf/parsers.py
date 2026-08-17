"""
This file hosts the function that parses the date from the URL to feed into the ecmwf open-data client.

(C) Eric J. Drewitz 2025-2026
"""

def parse_date(url,
                model):
    
    """
    This function parses the date from the download URL and returns the date as a string in the format of 'YYYY-mm-dd'
    
    Required Arguments:
    
    1) url (String) - The url to parse.
    
    2) The model being used. 
    
    Optional Arguments:
    
    None
    
    Returns
    -------
    
    The date in string format 'YYYY-mm-dd'    
    """
    model = model.lower()
    
    if model == 'ifs' or model == 'ifs-wave' or model == 'ifs-ensemble':
        date = f"{url[-27]}{url[-26]}{url[-25]}{url[-24]}-{url[-23]}{url[-22]}-{url[-21]}{url[-20]}"
    
    elif model == 'aifs-single':
        date = f"{url[-35]}{url[-34]}{url[-33]}{url[-32]}-{url[-31]}{url[-30]}-{url[-29]}{url[-28]}"
    
    else:
        date = f"{url[-32]}{url[-31]}{url[-30]}{url[-29]}-{url[-28]}{url[-27]}-{url[-26]}{url[-25]}"
        
    return date