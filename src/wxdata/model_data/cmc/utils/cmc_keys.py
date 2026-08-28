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
        
def hrdps_variable_keys(variable):
    
    """
    This function returns the variable in the filename to make our HTTPS request.
    
    Required Argument:
    
    1) variable (String) - The variable the user wants to query.
    
    ***Variable List***
    
        'air density'
        'absolute vorticity'
        'albedo'
        'blowing snow'
        'boundary layer height'
        'cape'
        'character of precipitation'
        'cloud water'
        'conditional freezing precipitation'
        'conditional amount of liquid precipitation'
        'conditional amount of solid ice pellets'
        'conditional amount of solid snow'
        'conditional precipitation rate'
        'convective precipitation'
        'dew point depression'
        'dew point'
        'dominant precipitation type'
        'downward longwave radiation flux'
        'downward shortwave radiation flux'
        'geopotential height'
        'latent heat net flux'
        'lifted index'
        'mean sea level pressure'
        'net longwave radiation flux'
        'net shortwave radiation flux'
        'snow level height'
        'humidex'
        'orography'
        'precipitation rate'
        'precipitation type'
        'pressure'
        'probability of blowing snow'
        'probability of drizzle'
        'probability of freezing drizzle'
        'probability of freezing precipitation'
        'probability of freezing rain'
        'probability of ice pellets'
        'probability of liquid precipitation'
        'probability of precipitation'
        'probability of rain'
        'probability of snow squalls'
        'probability of snow'
        'probability of thunderstorms'
        'relative humidity'
        'sea ice fraction'
        'secondary precipitation type'
        'sensible heat net flux'
        'showalter index'
        'skin temperature'
        'sky state'
        'snow density'
        'snow depth water equivalent'
        'snow depth'
        'soil temperature'
        'soil volumetric ice content'
        'specific humidity'
        'storm relative helicity'
        'surface runoff'
        'sweat index'
        'temperature'
        'thickness'
        'total cloud cover'
        'total precipitation intensity index'
        'total precipitation'
        'upward longwave radiation flux'
        'upward shortwave radiation flux'
        'uv index'
        'uv index (clear sky)'
        'ventilation index'
        'vertical wind shear'
        'vertical velocity'
        'visibility through ice fog'
        'visibility through liquid fog'
        'land sea mask'
        'wind chill'
        'wind direction'
        'wind gust'
        'wind speed'
        'u-wind component'
        'v-wind component'
    
    Optional Arguments: None
    
    Returns
    -------
    
    The variable in the format on the filename to make our HTTPS request.     
    """
    
    variables = {
        
        'air density':'HRDPS_DEN',
        'absolute vorticity':'HRDPS_ABSV',
        'albedo':'HRDPS_ALBDO',
        'blowing snow':'HRDPS-WEonG_BLSN',
        'boundary layer height':'HRDPS_HPBL',
        'cape':'HRDPS_CAPE',
        'character of precipitation':'HRDPS-WEonG_CHARPCPN',
        'cloud water':'HRDPS_CWAT',
        'conditional freezing precipitation':'HRDPS-WEonG_CONDAFZPCPN',
        'conditional amount of liquid precipitation':'HRDPS-WEonG_CONDALPCPN',
        'conditional amount of solid ice pellets':'HRDPS-WEonG_CONDAPL',
        'conditional amount of solid snow':'HRDPS-WEonG_CONDASSN',
        'conditional precipitation rate':'HRDPS-WEonG_CONDAPCPN',
        'convective precipitation':'HRDPS_ACPCP',
        'dew point depression':'HRDPS_DEPR',
        'dew point':'HRDPS_DPT',
        'dominant precipitation type':'HRDPS-WEonG_DMNTPCPNTYPE',
        'downward longwave radiation flux':'HRDPS_DLWRF',
        'downward shortwave radiation flux':'HRDPS_DSWRF',
        'geopotential height':'HRDPS_HGT',
        'latent heat net flux':'HRDPS_LHTFL',
        'lifted index':'HRDPS_LFTX',
        'mean sea level pressure':'HRDPS_PRMSL',
        'net longwave radiation flux':'HRDPS_NLWRS',
        'net shortwave radiation flux':'HRDPS_NSWRS',
        'snow level height':'HRDPS-WEonG_HGTSNLVL',
        'humidex':'HRDPS_Humidex',
        'orography':'HRDPS_ORGPHY',
        'precipitation rate':'HRDPS_PRATE',
        'precipitation type':'HRDPS-WEonG_PCPNTYPE',
        'pressure':'HRDPS_PRES',
        'probability of blowing snow':'HRDPS-WEonG_PROBBLSN',
        'probability of drizzle':'HRDPS-WEonG_PROBDZ',
        'probability of freezing drizzle':'HRDPS-WEonG_PROBFZDZ',
        'probability of freezing precipitation':'HRDPS-WEonG_PROBFZPCPN',
        'probability of freezing rain':'HRDPS-WEonG_PROBFZRA',
        'probability of ice pellets':'HRDPS-WEonG_PROBPL',
        'probability of liquid precipitation':'HRDPS-WEonG_PROBLPCPN',
        'probability of precipitation':'HRDPS-WEonG_PROBPCPN',
        'probability of rain':'HRDPS-WEonG_PROBRA',
        'probability of snow squalls':'HRDPS-WEonG_PROBSNSQ',
        'probability of snow':'HRDPS-WEonG_PROBSN',
        'probability of thunderstorms':'HRDPS-WEonG_PROBTSOCRNC',
        'relative humidity':'HRDPS_RH',
        'sea ice fraction':'HRDPS_ICEC',
        'secondary precipitation type':'HRDPS-WEonG_SCNDPCPNTYPE',
        'sensible heat net flux':'HRDPS_SHTFL',
        'showalter index':'HRDPS_SHWINX',
        'skin temperature':'HRDPS_SKINT',
        'sky state':'HRDPS-WEonG_SKSTATE',
        'snow density':'HRDPS_SDEN',
        'snow depth water equivalent':'HRDPS_SDWE',
        'snow depth':'HRDPS_SNOD',
        'soil temperature':'HRDPS_TSOIL',
        'soil volumetric ice content':'HRDPS_SOILVIC',
        'specific humidity':'HRDPS_SPFH',
        'storm relative helicity':'HRDPS_HLCY',
        'surface runoff':'HRDPS_SFCWRO',
        'sweat index':'HRDPS_SWEAT',
        'temperature':'HRDPS_TMP',
        'thickness':'HRDPS_HGT',
        'total cloud cover':'HRDPS_TCDC',
        'total precipitation intensity index':'HRDPS-WEonG_TPCPNINTSTI',
        'total precipitation':'HRDPS_APCP',
        'upward longwave radiation flux':'HRDPS_ULWRF',
        'upward shortwave radiation flux':'HRDPS_USWRF',
        'uv index':'HRDPS_UVI',
        'uv index (clear sky)':'HRDPS_UVIUCS',
        'ventilation index':'HRDPS_VI',
        'vertical wind shear':'HRDPS_VWSH',
        'vertical velocity':'HRDPS_VVEL',
        'visibility through ice fog':'HRDPS-WEonG_VISIFG',
        'visibility through liquid fog':'HRDPS-WEonG_VISLFG',
        'land sea mask':'HRDPS-WEonG_WTRLANMASK',
        'wind chill':'HRDPS_WCF',
        'wind direction':'HRDPS_WDIR',
        'wind gust':'HRDPS_GUST',
        'wind speed':'HRDPS_WIND',
        'u-wind component':'HRDPS_UGRD',
        'v-wind component':'HRDPS_VGRD'
    }
    
    try:
        return variables[variable]
    except Exception as e:
        _invalid_key(variable)
        
        
def cansips_variable_keys(variable):
    
    """
    This function returns the variable in the filename to make our HTTPS request.
    
    Required Argument:
    
    1) variable (String) - The variable the user wants to query.
    
    ***Variable List***
    
        'temperature'
        'geopotential height'
        'precipitation'
        'precipitation rate'
        'pressure'
        'sea surface height'
        'sea surface temperature'
        'u-wind component'
        'v-wind component'
        
    Optional Arguments: None
    
    Returns
    -------
    
    The variable in the format on the filename to make our HTTPS request.  
    """
    
    variables = {
        
        'temperature':'AirTemp',
        'geopotential height':'GeopotentialHeight',
        'precipitation':'PrecipAccum',
        'precipitation rate':'PrecipRate',
        'pressure':'Pressure',
        'sea surface height':'SeaSfcHeight',
        'sea surface temperature':'WaterTemp',
        'u-wind component':'WindU',
        'v-wind component':'WindV'
    }
    
    try:
        return variables[variable]
    except Exception as e:
        _invalid_key(variable)
      
def cansips_hindcast_keys(variable):
    
    """
    This function returns the variable in the filename to make our HTTPS request.
    
    Required Argument:
    
    1) variable (String) - The variable the user wants to query.
    
    ***Variable List***
    
        'temperature'
        'geopotential height'
        'precipitation rate'
        'pressure'
        'sea surface height'
        'sea surface temperature'
        'u-wind component'
        'v-wind component'
        
    Optional Arguments: None
    
    Returns
    -------
    
    The variable in the format on the filename to make our HTTPS request.  
    
    
    """
    
    variables = {
        
        'temperature':'AirTemp',
        'geopotential height':'GeopotentialHeight',
        'precipitation rate':'PrecipRate',
        'pressure':'Pressure',
        'sea surface height':'SeaSfcHeight',
        'sea surface temperature':'WaterTemp',
        'u-wind component':'WindU',
        'v-wind component':'WindV'
    }
    
    try:
        return variables[variable]
    except Exception as e:
        _invalid_key(variable)  
        
def geps_variable_keys(variable):
    
    """
    This function returns the variable in the filename to make our HTTPS request.
    
    Required Argument:
    
    1) variable (String) - The variable the user wants to query.
    
    ***Variable List***
    
        'freezing rain accumulation'
        'ice pellets accumulation'
        'total convective precipitation'
        'rain accumulation'
        'snow accumulation'
        'cape'
        'cin'
        'downward longwave radiation flux'
        'downward shortwave radiation flux'
        'geopotential height'
        'sea ice thickness'
        'latent heat net flux'
        'outgoing longwave radiation'
        'pressure'
        'mean sea level pressure'
        'precipitable water'
        'relative humidity'
        'surface runoff'
        'sensible heat net flux'
        'snow depth'
        'specific humidity'
        'soil moisture'
        'total cloud cover'
        'maximum temperature'
        'minimum temperature'
        'temperature'
        'soil temperature'
        'u-wind component'
        'v-wind component'
        'upward longwave radiation flux'
        'upward shortwave radiation flux'
        'vertical velocity'
        'wind speed'
        
    Optional Arguments: None
    
    Returns
    -------
    
    The variable in the format on the filename to make our HTTPS request.  
    """
    
    variables = {
        
        'freezing rain accumulation':'AFRAIN',
        'ice pellets accumulation':'AICEP',
        'total convective precipitation':'APCP',
        'rain accumulation':'ARAIN',
        'snow accumulation':'ASNOW',
        'cape':'CAPE',
        'cin':'CIN',
        'downward longwave radiation flux':'HRDPS_DLWRF',
        'downward shortwave radiation flux':'HRDPS_DSWRF',
        'geopotential height':'HGT',
        'sea ice thickness':'ICETK',
        'latent heat net flux':'LHTFL',
        'outgoing longwave radiation':'OLR',
        'pressure':'PRES',
        'mean sea level pressure':'PRMSL',
        'precipitable water':'PWAT',
        'relative humidity':'RH',
        'surface runoff':'SFCWRO',
        'sensible heat net flux':'HRDPS_SHTFL',
        'snow depth':'SNOD',
        'specific humidity':'SPFH',
        'soil moisture':'SWAT',
        'total cloud cover':'TCDC',
        'maximum temperature':'TMAX',
        'minimum temperature':'TMIN',
        'temperature':'TMP',
        'soil temperature':'TSOIL',
        'u-wind component':'UGRD',
        'v-wind component':'VGRD',
        'upward longwave radiation flux':'ULWRF',
        'upward shortwave radiation flux':'USWRF',
        'vertical velocity':'VVEL',
        'wind speed':'WIND'
        
    }

    try:
        return variables[variable]
    except Exception as e:
        _invalid_key(variable)

