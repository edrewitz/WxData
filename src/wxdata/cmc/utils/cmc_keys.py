"""
This file hosts the functions that map the user input to he variable keys to the filenames on https://dd.weather.gc.ca/

(C) Eric J. Drewitz 2025-2026
"""

def gdps_rdps_variable_keys(variable):
    
    """
    This function maps the variables from the user selection to the names on the files at https://dd.weather.gc.ca/
    
    Required Arguments:
    
    1) variable (String) - Variable name.
    
    Optional Arguments: None
    
    Returns
    -------
    
    The variable name as it appears on the files at https://dd.weather.gc.ca/     
    """
    
    variables = {
        
        'absolute vorticity':'AbsoluteVorticity',
        'relative vorticity':'RelativeVorticity',
        'temperature':'AirTemp',
        'albedo':'Albedo',
        'cape':'CAPE',
        'cin':'CIN',
        'cloud water':'CloudWater',
        'total convective precipitation':'ConvectivePrecip-Accum',
        'dew point depression':'DewPointDepression',
        'dew point':'DewPoint',
        'downward longwave radiation flux':'DownwardLongwaveRadiationFlux-Accum',
        'downward shortwave radiation flux':'DownwardShortwaveRadiationFlux-Accum',
        'geopotential height':'GeopotentialHeight',
        'humidex':'Humidex',
        'k index':'KIndex',
        'land water proportion':'LandWaterProportion',
        'latent heat net flux':'LatentHeatNetFlux',
        'lifted index':'LiftedIndex-MU-VT',
        'maximum wind gust':'WindGust-Max',
        'minimum wind gust':'WindGust-Min',
        'net longwave radiation flux':'NetLongwaveRadiationFlux-Accum',
        'net shortwave radiation flux':'NetShortwaveRadiationFlux-Accum',
        'ozone mixing ratio':'O3MixingRatio',
        'ozone':'O3',
        'boundary layer height':'PlanetaryBoundaryLayerHeight',
        'precipitation type':'PrecipType-Instant',
        'pressure':'Pressure',
        'radiative temperature':'RadiativeTemp',
        'relative humidity':'RelativeHumidity',
        'surface runoff':'Runoff-Accum',
        'sea ice fraction':'SeaIceFraction',
        'sea surface temperature':'SeaWaterTemp',
        'sensible heat net flux':'SensibleHeatNetFlux',
        'showalter index':'ShowalterIndex',
        'snow density':'SnowDensity',
        'snow depth':'SnowDepth',
        'soil temperature':'SoilTemp',
        'soil volumetric ice content':'SoilVolumetricIceContent',
        'soil volumetric water content':'SoilVolumetricWaterContent',
        'specific humidity':'SpecificHumidity',
        'thickness':'Thickness',
        'total cloud cover':'TotalCloudCover',
        'total totals index':'TotalTotalsIndex',
        'uv index (clear sky)':'UVIndex-ClearSky',
        'uv index':'UVIndex',
        'upward longwave radiation flux':'UpwardLongwaveRadiationFlux',
        'vertical velocity':'VerticalVelocity',
        'wind chill':'WindChill',
        'wind direction':'WindDir',
        'wind gust':'WindGust',
        'wind speed':'WindSpeed',
        'u-component of wind':'WindU',
        'v-component of wind':'WindV'
    }
    
    return variables[variable]

