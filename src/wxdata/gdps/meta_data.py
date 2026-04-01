"""
This file hosts the functions that map the various meta data for HTTPS request purposes,

(C) Eric J. Drewitz 2025-2026
"""

def meta_keys(variable):
    
    """
    This function maps the variable to the proper GDPS variable key for HTTPS request purposes
    
    Required Arguments:
    
    1) variable (String) - Variable name. 
    
    Returns
    -------
    
    GDPS Variable Key for HTTP Request    
    """
    
    variable = variable.lower()
    
    keys = {
        'absolute vorticity':'AbsoluteVorticity_Isbl',
        'air temperature':'AirTemp_Isbl',
        '2-meter air temperature':'AirTemp_AGL-2m',
        '40-meter air temperature':'AirTemp_AGL-40m',
        '80-meter air temperature':'AirTemp_AGL-80m',
        '120-meter air temperature':'AirTemp_AGL-120m',
        'albedo':'Albedo_Sfc',
        'cape':'CAPE_Sfc',
        'cin':'CIN_Sfc',
        'cloud water':'CloudWater_EAtm',
        'convective precipitation accumulation':'ConvectivePrecip-Accum_Sfc',
        'dew point depression':'DewPointDepression_Isbl',
        '2-meter dew point depression':'DewPointDepression_AGL-2m',
        '2-meter dew point':'DewPoint_AGL-2m',
        'downward longwave radiation flux accumulation':'DownwardLongwaveRadiationFlux-Accum_Sfc',
        'downward shortwave radiation flux accumulation':'DownwardShortwaveRadiationFlux-Accum_NTAtm',
        'geopotential height':'GeopotentialHeight_Isbl',
        'surface geopotential height':'GeopotentialHeight_Sfc',
        'humidex':'Humidex_Sfc',
        'k-index':'KIndex_Sfc',
        'land water proportion':'LandWaterProportion_Sfc',
        'latent heat net flux':'LatentHeatNetFlux_Sfc',
        'lifted index':'LiftedIndex-MU-VT_Isbl',
        'net longwave radiation flux accumulation':'NetLongwaveRadiationFlux-Accum_Sfc',
        'net shortwave radiation flux accumulation':'NetShortwaveRadiationFlux-Accum_Sfc',
        'ozone mass mixing ratio':'O3MixingRatio',
        'total ozone':'O3_EAtm',
        'planetary boundary layer height':'PlanetaryBoundaryLayerHeight_Sfc',
        'precipitation type':'PrecipType-Instant_Sfc'
    }
    
