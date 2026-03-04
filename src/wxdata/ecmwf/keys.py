"""
This file hosts the functions that map plain name variable keys from the optional arguments into the keys used by ECMWF to query

(C) Eric J. Drewitz 2025-2026
"""

def get_levels(levels):
    
    """
    This function QC's the list of pressure levels provided by the user
    
    Required Arguments:
    
    1) levels (Integer List) - A list of pressure levels.
    
    Optional Arguments: None
    
    Returns
    -------
    
    A list of pressure levels
    """
    
    pressure_levels = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]
    
    levs = []
    for l in levels:
        if l not in pressure_levels:
            print(f"{l} hPa is not a valid level - Skipping")
        else:
            levs.append(l)
    
    return levs


def ifs_var_keys(var_list):
    
    """
    This function iterates through the variable list and returns a list of keys in the format used by ECMWF.
    These keys will then be passed in as a list for querying via the ecmwf-opendata client
    
    The keys in this function will be specific to the ECMWF IFS
    
    Required Arguments:
    
    1) var_list (String List) - The list of variable keys
    
        Valid Variable Keys
        -------------------
    
        'Geopotential (step 0)'
        'Standard deviation of sub-gridscale orography (step 0)'
        '10-meter u-wind component'
        '10-meter v-wind component'
        '100-meter u-wind component'
        '100-meter v-wind component'
        'maximum 10-meter wind gust step 0'
        'maximum 10-meter wind gust steps 3-144'
        '2-meter temperature'
        '2-meter dewpoint temperature'
        'mean sea level pressure'
        'mean zero-crossing wave period'
        'mean wave direction'
        'mean wave period'
        'peak wave period'
        'significant wave height'
        'runoff'
        'total precipitation'
        'surface pressure'
        'total column vertically integrated water vapor'
        'total cloud cover'
        'snow depth water equivalent'
        'snowfall water equivalent'
        'land sea mask'
        'volumetric soil moisture content'
        'soil temperature'
        'most unstable cape'
        'snow albedo'
        '3-hour minimum 2-meter temperature'
        '3-hour maximum 2-meter temperature'
        '6-hour minimum 2-meter temperature'
        '6-hour maximum 2-meter temperature'
        'total precipitation rate'
        'precipitation type'
        'top net longwave thermal radiation'
        'snow density'
        'surface net longwave thermal radiation'
        'surface net shortwave solar radiation'
        'surface shortwave radiation downward'
        'surface longwave radiation downward'
        'northward turbulent surface stress'
        'eastward turbulent surface stress'
        'eastward surface sea water velocity'
        'northward surface sea water velocity'
        'sea ice thickness'
        'sea surface height'
        'divergence'
        'geopotential height'
        'specific humidity'
        'relative humidity'
        'temperature'
        'u-wind component'
        'v-wind component'
        'vertical velocity'
        'relative vorticity'
    
    Optional Arguments: None
    
    Returns
    -------
    
    A list of variable keys in the format used by ECMWF    
    """
    
    ifs_keys = {
        
        'Geopotential (step 0)':'z',
        'Standard deviation of sub-gridscale orography (step 0)':'sdor',
        '10-meter u-wind component':'10u',
        '10-meter v-wind component':'10v',
        '100-meter u-wind component':'100u',
        '100-meter v-wind component':'100v',
        'maximum 10-meter wind gust step 0':'10fg',
        'maximum 10-meter wind gust steps 3-144':'10fg3',
        '2-meter temperature':'2t',
        '2-meter dewpoint temperature':'2d',
        'mean sea level pressure':'msl',
        'mean zero-crossing wave period':'mp2',
        'mean wave direction':'mwd',
        'mean wave period':'mwp',
        'peak wave period':'pp1d',
        'significant wave height':'swh',
        'runoff':'ro',
        'total precipitation':'tp',
        'surface pressure':'sp',
        'total column vertically integrated water vapor':'tcwv',
        'total cloud cover':'tcc',
        'snow depth water equivalent':'sd',
        'snowfall water equivalent':'sf',
        'land sea mask':'lsm',
        'volumetric soil moisture content':'vsw',
        'soil temperature':'sot',
        'most unstable cape':'mucape',
        'snow albedo':'asn',
        '3-hour minimum 2-meter temperature':'mn2t3',
        '3-hour maximum 2-meter temperature':'mx2t3',
        '6-hour minimum 2-meter temperature':'mn2t6',
        '6-hour maximum 2-meter temperature':'mx2t6',
        'total precipitation rate':'tprate',
        'precipitation type':'ptype',
        'top net longwave thermal radiation':'ttr',
        'snow density':'rsn',
        'surface net longwave thermal radiation':'str',
        'surface net shortwave solar radiation':'ssr',
        'surface shortwave radiation downward':'ssrd',
        'surface longwave radiation downward':'strd',
        'northward turbulent surface stress':'nsss',
        'eastward turbulent surface stress':'ewss',
        'eastward surface sea water velocity':'sve',
        'northward surface sea water velocity':'svn',
        'sea ice thickness':'sithick',
        'sea surface height':'zos',
        'divergence':'d',
        'geopotential height':'gh',
        'specific humidity':'q',
        'relative humidity':'r',
        'temperature':'t',
        'u-wind component':'u',
        'v-wind component':'v',
        'vertical velocity':'w',
        'relative vorticity':'vo'
    }
    
    params = []
    for key in var_list:
        if key in ifs_keys:
            params.append(ifs_keys[key])
        else:
            print(f"'{key}' Key not found in valid parameter list - skipping this variable")
            
    return params

def aifs_var_keys(var_list):
    
    """
    This function iterates through the variable list and returns a list of keys in the format used by ECMWF.
    These keys will then be passed in as a list for querying via the ecmwf-opendata client
    
    The keys in this function will be specific to the ECMWF AIFS
    
    Required Arguments:
    
    1) var_list (String List) - The list of variable keys
    
        Valid Variable Keys
        -------------------
    
        'geopotential'
        'total column water'
        'mean sea level pressure'
        'standard deviation of sub-gridscale orography'
        'slope of sub-gridscale orography'
        '10-meter u-wind component'
        '10-meter v-wind component'
        '2-meter temperature'
        '2-meter dew point'
        'surface shortwave radiation downward'
        'land sea mask'
        'surface longwave radiation downward'
        'low cloud cover'
        'mid-level cloud cover'
        'high cloud cover'
        'runoff water equivalent'
        'convective precipitation'
        'snowfall water equivalent'
        'total cloud cover'
        'total precipitation'
        '100-meter u-wind component'
        '100-meter v-wind component'
        'skin temperature'
        'surface pressure'
        'specific humidity'
        'relative humidity'
        'temperature'
        'u-wind component'
        'v-wind component'
        'vertical velocity'
        'volumetric soil moisture content'
        'soil temperature'
    
    Optional Arguments: None
    
    Returns
    -------
    
    A list of variable keys in the format used by ECMWF    
    """
    
    aifs_keys = {
        'geopotential':'z',
        'total column water':'tcw',
        'mean sea level pressure':'msl',
        'standard deviation of sub-gridscale orography':'sdor',
        'slope of sub-gridscale orography':'slor',
        '10-meter u-wind component':'10u',
        '10-meter v-wind component':'10v',
        '2-meter temperature':'2t',
        '2-meter dew point':'2d',
        'surface shortwave radiation downward':'ssrd',
        'land sea mask':'lsm',
        'surface longwave radiation downward':'strd',
        'low cloud cover':'lcc',
        'mid-level cloud cover':'mcc',
        'high cloud cover':'hcc',
        'runoff water equivalent':'rowe',
        'convective precipitation':'cp',
        'snowfall water equivalent':'sf',
        'total cloud cover':'tcc',
        'total precipitation':'tp',
        '100-meter u-wind component':'100u',
        '100-meter v-wind component':'100v',
        'skin temperature':'skt',
        'surface pressure':'sp',
        'specific humidity':'q',
        'relative humidity':'r',
        'temperature':'t',
        'u-wind component':'u',
        'v-wind component':'v',
        'vertical velocity':'w',
        'volumetric soil moisture content':'vsw',
        'soil temperature':'sot'
    }
    
    params = []
    for key in var_list:
        if key in aifs_keys:
            params.append(aifs_keys[key])
        else:
            print(f"'{key}' Key not found in valid parameter list - skipping this variable")
            
    return params
            