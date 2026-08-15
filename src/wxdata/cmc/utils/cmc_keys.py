"""
This file hosts the functions that map the user input to he variable keys to the filenames on https://dd.weather.gc.ca/

(C) Eric J. Drewitz 2025-2026
"""

import sys

def _invalid_key(variable):
    
    """
    Returns an error message for invalid variable keys.
    """
    
    print(f"Error: '{variable}' is not a valid variable key.\nPlease try again")
    sys.exit(1)

def gdps_rdps_variable_keys(variable):
    
    """
    This function maps the variables from the user selection to the names on the files at https://dd.weather.gc.ca/
    
    Required Arguments:
    
    1) variable (String) - Variable name.
    
    ***List of Variables***
    
        'absolute vorticity'
        'relative vorticity'
        'temperature'
        'albedo'
        'cape'
        'cin'
        'cloud water'
        'total convective precipitation'
        'total precitation 12hr'
        'total precitation 1hr'
        'total precitation 24hr'
        'total precitation 3hr'
        'total precitation 6hr'
        'total precitation'
        'dew point depression'
        'dew point'
        'downward longwave radiation flux'
        'downward shortwave radiation flux'
        'freezing rain accumulation 12hr'
        'freezing rain accumulation 1hr'
        'freezing rain accumulation 24hr'
        'freezing rain accumulation 3hr'
        'freezing rain accumulation 6hr'
        'freezing rain accumulation total'
        'geopotential height'
        'humidex'
        'ice pellets accumulation 12hr'
        'ice pellets accumulation 1hr'
        'ice pellets accumulation 24hr'
        'ice pellets accumulation 3hr'
        'ice pellets accumulation 6hr'
        'ice pellets accumulation total'
        'k index'
        'land water proportion'
        'latent heat net flux'
        'lifted index'
        'maximum wind gust'
        'minimum wind gust'
        'net longwave radiation flux'
        'net shortwave radiation flux'
        'ozone mixing ratio'
        'ozone'
        'boundary layer height'
        'precipitation type'
        'precipitation rate'
        'pressure'
        'radiative temperature'
        'rain accumulation 12hr'
        'rain accumulation 1hr'
        'rain accumulation 24hr'
        'rain accumulation 3hr'
        'rain accumulation 6hr'
        'rain accumulation total'
        'relative humidity'
        'surface runoff'
        'sea ice fraction'
        'sea surface temperature'
        'sensible heat net flux'
        'showalter index'
        'snow density'
        'snow depth'
        'snow accumulation 12hr'
        'snow accumulation 1hr'
        'snow accumulation 24hr'
        'snow accumulation 3hr'
        'snow accumulation 6hr'
        'snow accumulation total'
        'soil temperature'
        'soil volumetric ice content'
        'soil volumetric water content'
        'specific humidity'
        'storm relative helicity'
        'storm severity index'
        'sweat index'
        'seeing index'
        'sky transparency index'
        'thickness'
        'total cloud cover'
        'total totals index'
        'uv index (clear sky)'
        'uv index'
        'upward longwave radiation flux'
        'vertical velocity'
        'wind chill'
        'wind direction'
        'wind gust'
        'wind speed'
        'u-component of wind'
        'v-component of wind'
        'vertical wind shear'
    
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
        'total precitation 12hr':'Precip-Accum12h',
        'total precitation 1hr':'Precip-Accum1h',
        'total precitation 24hr':'Precip-Accum24h',
        'total precitation 3hr':'Precip-Accum3h',
        'total precitation 6hr':'Precip-Accum6h',
        'total precitation':'Precip-Accum',
        'dew point depression':'DewPointDepression',
        'dew point':'DewPoint',
        'downward longwave radiation flux':'DownwardLongwaveRadiationFlux-Accum',
        'downward shortwave radiation flux':'DownwardShortwaveRadiationFlux-Accum',
        'freezing rain accumulation 12hr':'FreezingRain-Accum12h',
        'freezing rain accumulation 1hr':'FreezingRain-Accum1h',
        'freezing rain accumulation 24hr':'FreezingRain-Accum24h',
        'freezing rain accumulation 3hr':'FreezingRain-Accum3h',
        'freezing rain accumulation 6hr':'FreezingRain-Accum6h',
        'freezing rain accumulation total':'FreezingRain-Accum',
        'geopotential height':'GeopotentialHeight',
        'humidex':'Humidex',
        'ice pellets accumulation 12hr':'IcePellets-Accum12h',
        'ice pellets accumulation 1hr':'IcePellets-Accum1h',
        'ice pellets accumulation 24hr':'IcePellets-Accum24h',
        'ice pellets accumulation 3hr':'IcePellets-Accum3h',
        'ice pellets accumulation 6hr':'IcePellets-Accum6h',
        'ice pellets accumulation total':'IcePellets-Accum',
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
        'precipitation rate':'PrecipRate',
        'pressure':'Pressure',
        'radiative temperature':'RadiativeTemp',
        'rain accumulation 12hr':'Rain-Accum12h',
        'rain accumulation 1hr':'Rain-Accum1h',
        'rain accumulation 24hr':'Rain-Accum24h',
        'rain accumulation 3hr':'Rain-Accum3h',
        'rain accumulation 6hr':'Rain-Accum6h',
        'rain accumulation total':'Rain-Accum',
        'relative humidity':'RelativeHumidity',
        'surface runoff':'Runoff-Accum',
        'sea ice fraction':'SeaIceFraction',
        'sea surface temperature':'SeaWaterTemp',
        'sensible heat net flux':'SensibleHeatNetFlux',
        'showalter index':'ShowalterIndex',
        'snow density':'SnowDensity',
        'snow depth':'SnowDepth',
        'snow accumulation 12hr':'Snow-Accum12h',
        'snow accumulation 1hr':'Snow-Accum1h',
        'snow accumulation 24hr':'Snow-Accum24h',
        'snow accumulation 3hr':'Snow-Accum3h',
        'snow accumulation 6hr':'Snow-Accum6h',
        'snow accumulation total':'Snow-Accum',
        'soil temperature':'SoilTemp',
        'soil volumetric ice content':'SoilVolumetricIceContent',
        'soil volumetric water content':'SoilVolumetricWaterContent',
        'specific humidity':'SpecificHumidity',
        'storm relative helicity':'StormRelativeHelicity',
        'storm severity index':'StormSeverityIndex',
        'sweat index':'SWEATIndex',
        'seeing index':'SeeingIndex',
        'sky transparency index':'SkyTransparencyIndex',
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
        'v-component of wind':'WindV',
        'vertical wind shear':'VerticalWindShear'
    }
    
    try:
        return variables[variable]
    except Exception as e:
        _invalid_key(variable)
        


