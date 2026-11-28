"""
This file hosts the functions needed for the interface to query variables.

(C) Eric J. Drewitz 2025-2026
"""

import sys

def query_variables(variable):
    
    """
    This function maps the variable name to the expression for our request URL
    
    Required Arguments:
    
    1) variable (String) - The variable name.
    
    ***Variables***
    
    'dew point temperature'
    'dew point temperature - 15 minute observation'
    'dew point temperature - 1 hour average'
    'dew point temperature change - 1 hour'
    'relative humidity'
    'relative humidity - 15 minute observation'
    'relative humidity - 1 hour average'
    'relative humidity change - 1 hour'
    'water vapor mixing ratio'
    'water vapor mixing ratio - 15 minute observation'
    'water vapor mixing ratio change - 1 hour'
    'specific humidity'
    'specific humidity - 15 minute observation'
    'specific humidity - 1 hour average'
    'specific humidity change - 1 hour'
    'dew point depression'
    'dew point depression - 15 minute observation'
    'dew point depression - 1 hour average'
    'dew point depression change - 1 hour'
    'absolute humidity'
    'absolute humidity - 15 minute observation'
    'absolute humidity - 1 hour average'
    'absolute humidity change - 1 hour'
    'altimeter'
    'altimeter - 15 minute observation'
    'altimeter change - 1 hour'
    'pressure change - 3 hour'
    'character of pressure change - 3 hour'
    'sea level pressure'
    'station pressure'
    'station pressure - 15 minute observation'
    'temperature'
    'temperature - 15 minute observation'
    'temperature - 1 hour average'
    'temperature change - 1 hour'
    'virtual temperature'
    'virtual temperature - 15 minute observation'
    'virtual temperature - 1 hour average'
    'virtual temperature change - 1 hour'
    'wind direction'
    'wind direction - 15 minute average'
    'wind direction - 1 hour average'
    'wind direction - 24 hour average'
    'wind direction mean vector - 15 minute'
    'wind direction standard deviation - 15 minute'
    'mean unit vector wind direction - 15 minute'
    'wind speed'
    'wind speed - 15 minute observation'
    'wind speed - 1 hour average'
    'wind speed - 24 hour average'
    'wind speed standard deviation - 15 minute'
    'u-component of wind'
    'u-component of wind - 1 hour average'
    'u-component of wind - 24 hour average'
    'u-component of wind mean unit vector wind - 15 minute'
    'u-component of wind standard deviation - 15 minute'
    'v-component of wind'
    'v-component of wind - 1 hour average'
    'v-component of wind - 24 hour average'
    'v-component of wind mean unit vector wind - 15 minute'
    'v-component of wind standard deviation - 15 minute'
    'visibility'
    'vertical visibility'
    'wmo station number'
    'station elevation'
    'latitude'
    'longitude'
    'data platform type'
    'platform true direction'
    'platform true speed'
    'correction flag'
    'total precipitation'
    'accumulated precipitation - 5 minute'
    'accumulated precipitation - 15 minute'
    'accumulated precipitation - 1 hour'
    'accumulated precipitation - 1 hour ASOS start time'
    'accumulated precipitation - 3 hour'
    'accumulated precipitation - 6 hour'
    'accumulated precipitation - 12 hour'
    'accumulated precipitation - 18 hour'
    'accumulated precipitation - 24 hour'
    'accumulated precipitation - monthly'
    'accumulated precipitation - since local midnight'
    'accumulated precipitation - since utc midnight'
    'accumulated precipitation - yesterday local calendar day'
    'accumulated precipitation - user-defined day'
    'user-defined day start - HHMM'
    'precipitation rate'
    'precipitation intensity'
    'precipitation type'
    'sky cover layer base'
    'height of the lowest cloud layer'
    'low level cloud type'
    'middle level cloud type'
    'high level cloud type'
    'fraction of sky covered by clouds'
    'minimum temperature - 24 hour'
    'maximum temperature - 24 hour'
    'fuel moisture'
    'fuel temperature'
    'soil moisture tension'
    'soil moisture percent'
    'soil moisture percent - 2 inch'
    'soil moisture percent - 4 inch'
    'soil moisture percent - 8 inch'
    'soil moisture percent - 20 inch'
    'soil moisture percent - 40 inch'
    'soil temperature'
    'soil temperature - 2 inch'
    'soil temperature - 4 inch'
    'soil temperature - 8 inch'
    'soil temperature - 20 inch'
    'soil temperature - 40 inch'
    'wind direction at gust'
    'wind gust'
    'maximum wind direction'
    'wind direction at hourly maximum wind speed'
    'maximum wind speed'
    'maximum wind speed - 1 hour'
    'maximum wind speed - 24 hour'
    'direction of primary swell waves'
    'primary swell wave height'
    'primary swell wave period'
    'direction of secondary swell waves'
    'secondary swell wave height'
    'secondary swell wave period'
    'sea surface temperature'
    'tidal departure from predicted level'
    'tide indicator'
    'wave height'
    'wave period'
    'wave steepness'
    'wind wave period'
    'wind wave height'
    'high resolution wave height'
    'equivalent wind speed at 10m'
    'equivalent wind speed at 20m'
    'snow cover'
    'snowfall - 6 hour'
    'snowfall - 24 hour'
    'diffuse solar radiation - instantaneous'
    'diffuse solar radiation - 5 minute average'
    'diffuse solar radiation - 15 minute average'
    'diffuse solar radiation - 1 hour average'
    'diffuse solar radiation - 24 hour average'
    'direct solar radiation - instantaneous'
    'direct solar radiation - 5 minute average'
    'direct solar radiation - 15 minute average'
    'direct solar radiation - 1 hour average'
    'direct solar radiation - 24 hour average'
    'global solar radiation - instantaneous'
    'global solar radiation - 5 minute average'
    'global solar radiation - 15 minute average'
    'global solar radiation - 1 hour average'
    'global solar radiation - 24 hour average'
    'photosynthetically active radiation'
    'solar radiation - unknown type'
    'dew point from tenths of a degree celsius'
    'temperature from tenths of a degree celsius'
    'wet bulb temperature'
    'gpsmet precipitable water vapor'
    'gpsmet total signal delay'
    'gpsmet dry signal delay'
    'gpsmet wet signal delay'
    'gpsmet mean weighted temperature'
    'gpsmet formal error'
    'gpsmet wet delay mapping function'
    'road temperature - sensor 1'
    'road temperature - sensor 2'
    'road temperature - sensor 3'
    'road temperature - sensor 4'
    'road liquid freeze temperature - sensor 1'
    'road liquid freeze temperature - sensor 2'
    'road liquid freeze temperature - sensor 3'
    'road liquid freeze temperature - sensor 4'
    'road liquid chem factor - sensor 1'
    'road liquid chem factor - sensor 2'
    'road liquid chem factor - sensor 3'
    'road liquid chem factor - sensor 4'
    'road liquid chem percent - sensor 1'
    'road liquid chem percent - sensor 2'
    'road liquid chem percent - sensor 3'
    'road liquid chem percent - sensor 4'
    'road liquid ice percent - sensor 1'
    'road liquid ice percent - sensor 2'
    'road liquid ice percent - sensor 3'
    'road liquid ice percent - sensor 4'
    'road liquid depth - sensor 1'
    'road liquid depth - sensor 2'
    'road liquid depth - sensor 3'
    'road liquid depth - sensor 4'
    'road state - sensor 1'
    'road state - sensor 2'
    'road state - sensor 3'
    'road state - sensor 4'
    'road sub-surface temperature - sensor 1'
    'road sub-surface temperature - sensor 2'
    'road sub-surface temperature - sensor 3'
    'road sub-surface temperature - sensor 4'
    'battery voltage'
    'secondary battery voltage'
    'river stage'
    'station specific number 1'
    'station specific number 2'
    'commissioned status'
    'station quality indicator'
    'door open-closed indicator'
    'rim heating on-off indicator'
    'precipitation bucket level'
    'precipitation rim temperature'
    'vibrating wire depth - 1'
    'vibrating wire depth - 2'
    'vibrating wire depth - 3'
    'water elevation relative to mean lower low water'
    'number of observation - 15 minute'
    'average seconds between observations in 15 minute period'
    'number of sky cover observations'
    'automated station type'
    'report type'
    'present weather'
    'sky cover'
    'station location'
    'subprovider'
    'time of 24-hour minimum temperature'
    'time of 24-hour maximum temperature'
    'first observation time in 15 minute period'
    'last observation time in 15 minute period'
    'raw metar message'
    
    Optional Arguments: None
    
    **Returns**
    
    The variable expression in the format needed for our request URL    
    """
    
    variables = {
        
        'dew point temperature':'TD',
        'dew point temperature - 15 minute observation':'TD15M',
        'dew point temperature - 1 hour average':'TD1H',
        'dew point temperature change - 1 hour':'TD1HCHG',
        'relative humidity':'RH',
        'relative humidity - 15 minute observation':'RH15M',
        'relative humidity - 1 hour average':'RH1H',
        'relative humidity change - 1 hour':'RH1HCHG',
        'water vapor mixing ratio':'WVMR',
        'water vapor mixing ratio - 15 minute observation':'WVMR15M',
        'water vapor mixing ratio change - 1 hour':'WVMR1HC',
        'specific humidity':'Q',
        'specific humidity - 15 minute observation':'Q15M',
        'specific humidity - 1 hour average':'Q1H',
        'specific humidity change - 1 hour':'Q1HCHG',
        'dew point depression':'DPD',
        'dew point depression - 15 minute observation':'DPD15M',
        'dew point depression - 1 hour average':'DPD1H',
        'dew point depression change - 1 hour':'DPD1HC',
        'absolute humidity':'AH',
        'absolute humidity - 15 minute observation':'AH15M',
        'absolute humidity - 1 hour average':'AH1H',
        'absolute humidity change - 1 hour':'AH1HCHG',
        'altimeter':'ALTSE',
        'altimeter - 15 minute observation':'ALTS15M',
        'altimeter change - 1 hour':'AL1HCHG',
        'pressure change - 3 hour':'PT3',
        'character of pressure change - 3 hour':'PT3CHR',
        'sea level pressure':'SLP',
        'station pressure':'P',
        'station pressure - 15 minute observation':'P15M',
        'temperature':'T',
        'temperature - 15 minute observation':'T15M',
        'temperature - 1 hour average':'T1H',
        'temperature change - 1 hour':'T1HCHG',
        'virtual temperature':'TV',
        'virtual temperature - 15 minute observation':'TV15M',
        'virtual temperature - 1 hour average':'TV1H',
        'virtual temperature change - 1 hour':'TV1HCHG',
        'wind direction':'DD',
        'wind direction - 15 minute average':'DD15M',
        'wind direction - 1 hour average':'DD1H',
        'wind direction - 24 hour average':'DD24H',
        'wind direction mean vector - 15 minute':'DDM15M',
        'wind direction standard deviation - 15 minute':'DDSD15M',
        'mean unit vector wind direction - 15 minute':'DDU15M',
        'wind speed':'FF',
        'wind speed - 15 minute observation':'FF15M',
        'wind speed - 1 hour average':'FF1H',
        'wind speed - 24 hour average':'FF24H',
        'wind speed standard deviation - 15 minute':'FFSD15M',
        'u-component of wind':'U',
        'u-component of wind - 1 hour average':'U1H',
        'u-component of wind - 24 hour average':'U24H',
        'u-component of wind mean unit vector wind - 15 minute':'U15M',
        'u-component of wind standard deviation - 15 minute':'USD15M',
        'v-component of wind':'V',
        'v-component of wind - 1 hour average':'V1H',
        'v-component of wind - 24 hour average':'V24H',
        'v-component of wind mean unit vector wind - 15 minute':'V15M',
        'v-component of wind standard deviation - 15 minute':'VSD15M',
        'visibility':'VIS',
        'vertical visibility':'VERTVIS',
        'wmo station number':'WMOID',
        'station elevation':'ELEV',
        'latitude':'LAT',
        'longitude':'LON',
        'data platform type':'PLATTYP',
        'platform true direction':'PLATDIR',
        'platform true speed':'PLATSPD',
        'correction flag':'CORR',
        'total precipitation':'PCPTOTL',
        'accumulated precipitation - 5 minute':'PCP5M',
        'accumulated precipitation - 15 minute':'PCP15M',
        'accumulated precipitation - 1 hour':'PCP1H',
        'accumulated precipitation - 1 hour ASOS start time':'PCP1HA',
        'accumulated precipitation - 3 hour':'PCP3H',
        'accumulated precipitation - 6 hour':'PCP6H',
        'accumulated precipitation - 12 hour':'PCP12H',
        'accumulated precipitation - 18 hour':'PCP18H',
        'accumulated precipitation - 24 hour':'PCP24H',
        'accumulated precipitation - monthly':'PCPMNTH',
        'accumulated precipitation - since local midnight':'PCPLM',
        'accumulated precipitation - since utc midnight':'PCPUTCM',
        'accumulated precipitation - yesterday local calendar day':'PCPCDAY',
        'accumulated precipitation - user-defined day':'PCPUDAY',
        'user-defined day start - HHMM':'UDSTART',
        'precipitation rate':'PCPRATE',
        'precipitation intensity':'PCPINT',
        'precipitation type':'PCPTYPE',
        'sky cover layer base':'SKYCVLB',
        'height of the lowest cloud layer':'LCLHT',
        'low level cloud type':'LLCTYPE',
        'middle level cloud type':'MLCTYPE',
        'high level cloud type':'HLCTYPE',
        'fraction of sky covered by clouds':'CLDFRAC',
        'minimum temperature - 24 hour':'T24MIN',
        'maximum temperature - 24 hour':'T24MAX',
        'fuel moisture':'FUELM',
        'fuel temperature':'FUELT',
        'soil moisture tension':'SOILM',
        'soil moisture percent':'SOILMP',
        'soil moisture percent - 2 inch':'SOILM2',
        'soil moisture percent - 4 inch':'SOILM4',
        'soil moisture percent - 8 inch':'SOILM8',
        'soil moisture percent - 20 inch':'SOILM20',
        'soil moisture percent - 40 inch':'SOILM40',
        'soil temperature':'SOILT',
        'soil temperature - 2 inch':'SOILT2',
        'soil temperature - 4 inch':'SOILT4',
        'soil temperature - 8 inch':'SOILT8',
        'soil temperature - 20 inch':'SOILT20',
        'soil temperature - 40 inch':'SOILT40',
        'wind direction at gust':'DDGUST',
        'wind gust':'FFGUST',
        'maximum wind direction':'DDMAX',
        'wind direction at hourly maximum wind speed':'DDMAX1H',
        'maximum wind speed':'FFMAX',
        'maximum wind speed - 1 hour':'FFMAX1H',
        'maximum wind speed - 24 hour':'FF24MAX',
        'direction of primary swell waves':'PSWDIR',
        'primary swell wave height':'PSWHT',
        'primary swell wave period':'PSWPER',
        'direction of secondary swell waves':'SSWDIR',
        'secondary swell wave height':'SSWHT',
        'secondary swell wave period':'SSWPER',
        'sea surface temperature':'SST',
        'tidal departure from predicted level':'TIDEDEP',
        'tide indicator':'TIDEIND',
        'wave height':'WAVEHT',
        'wave period':'WAVEPER',
        'wave steepness':'WAVESTP',
        'wind wave period':'WWVEPER',
        'wind wave height':'WWVEHT',
        'high resolution wave height':'HRWVEHT',
        'equivalent wind speed at 10m':'EQFF10M',
        'equivalent wind speed at 20m':'EQFF20M',
        'snow cover':'SNOWC',
        'snowfall - 6 hour':'SNOW6H',
        'snowfall - 24 hour':'SNOW24H',
        'diffuse solar radiation - instantaneous':'FSRDINS',
        'diffuse solar radiation - 5 minute average':'FSRD5M',
        'diffuse solar radiation - 15 minute average':'FSRD15M',
        'diffuse solar radiation - 1 hour average':'FSRD1H',
        'diffuse solar radiation - 24 hour average':'FSRD24H',
        'direct solar radiation - instantaneous':'DSRDINS',
        'direct solar radiation - 5 minute average':'DSRD5M',
        'direct solar radiation - 15 minute average':'DSRD15M',
        'direct solar radiation - 1 hour average':'DSRD1H',
        'direct solar radiation - 24 hour average':'DSRD24H',
        'global solar radiation - instantaneous':'GSRDINS',
        'global solar radiation - 5 minute average':'GSRD5M',
        'global solar radiation - 15 minute average':'GSRD15M',
        'global solar radiation - 1 hour average':'GSRD1H',
        'global solar radiation - 24 hour average':'GSRD24H',
        'photosynthetically active radiation':'PAR',
        'solar radiation - unknown type':'SOLRAD',
        'dew point from tenths of a degree celsius':'TD10C',
        'temperature from tenths of a degree celsius':'T10C',
        'wet bulb temperature':'TWB',
        'gpsmet precipitable water vapor':'PWV',
        'gpsmet total signal delay':'GPSTSD',
        'gpsmet dry signal delay':'GPSDSD',
        'gpsmet wet signal delay':'GPSWSD',
        'gpsmet mean weighted temperature':'GPSMWT',
        'gpsmet formal error':'GPSFE',
        'gpsmet wet delay mapping function':'GPSWDMF',
        'road temperature - sensor 1':'RDT1',
        'road temperature - sensor 2':'RDT2',
        'road temperature - sensor 3':'RDT3',
        'road temperature - sensor 4':'RDT4',
        'road liquid freeze temperature - sensor 1':'RDLFT1',
        'road liquid freeze temperature - sensor 2':'RDLFT2',
        'road liquid freeze temperature - sensor 3':'RDLFT3',
        'road liquid freeze temperature - sensor 4':'RDLFT4',
        'road liquid chem factor - sensor 1':'RDLCF1',
        'road liquid chem factor - sensor 2':'RDLCF2',
        'road liquid chem factor - sensor 3':'RDLCF3',
        'road liquid chem factor - sensor 4':'RDLCF4',
        'road liquid chem percent - sensor 1':'RDLCP1',
        'road liquid chem percent - sensor 2':'RDLCP2',
        'road liquid chem percent - sensor 3':'RDLCP3',
        'road liquid chem percent - sensor 4':'RDLCP4',
        'road liquid ice percent - sensor 1':'RDLIP1',
        'road liquid ice percent - sensor 2':'RDLIP2',
        'road liquid ice percent - sensor 3':'RDLIP3',
        'road liquid ice percent - sensor 4':'RDLIP4',
        'road liquid depth - sensor 1':'RDLDP1',
        'road liquid depth - sensor 2':'RDLDP2',
        'road liquid depth - sensor 3':'RDLDP3',
        'road liquid depth - sensor 4':'RDLDP4',
        'road state - sensor 1':'RDSTA1',
        'road state - sensor 2':'RDSTA2',
        'road state - sensor 3':'RDSTA3',
        'road state - sensor 4':'RDSTA4',
        'road sub-surface temperature - sensor 1':'RDSUBT1',
        'road sub-surface temperature - sensor 2':'RDSUBT2',
        'road sub-surface temperature - sensor 3':'RDSUBT3',
        'road sub-surface temperature - sensor 4':'RDSUBT4',
        'battery voltage':'BATVLT',
        'secondary battery voltage':'BATVLT2',
        'river stage':'RIVSTG',
        'station specific number 1':'STNSPC1',
        'station specific number 2':'STNSPC2',
        'commissioned status':'COMSTAT',
        'station quality indicator':'STAQUAL',
        'door open-closed indicator':'DOORIND',
        'rim heating on-off indicator':'HEATIND',
        'precipitation bucket level':'BUCKLEV',
        'precipitation rim temperature':'RIMT',
        'vibrating wire depth - 1':'VIBWD1',
        'vibrating wire depth - 2':'VIBWD2',
        'vibrating wire depth - 3':'VIBWD3',
        'water elevation relative to mean lower low water':'MLLW',
        'number of observation - 15 minute':'NOBS15M',
        'average seconds between observations in 15 minute period':'ASBO15M',
        'number of sky cover observations':'NOBSSC',
        'automated station type':'AUTOTYP',
        'report type':'REPTYPE',
        'present weather':'PRESWEA',
        'sky cover':'SKYCOV',
        'station location':'STALOC',
        'subprovider':'SUBPVDR',
        'time of 24-hour minimum temperature':'T24MINT',
        'time of 24-hour maximum temperature':'T24MAXT',
        'first observation time in 15 minute period':'FOT15M',
        'last observation time in 15 minute period':'LOT15M',
        'raw metar message':'RAWMTR'
    }
    
    try:
        return variables[variable]
    except Exception as e:
        print(f"Error {variable} is not a valid field.\nSystem Exit.")
        sys.exit(1)
        
        
def url_variables(variables):
    
    """
    This function builds the string of variables to be used in the URL request.
    
    Required Arguments:
    
    1) variables (String List) - A list of variables.
    
    Optional Arguments: None
    
    **Returns**
    
    A string of variables in the format needed to make our HTTP request.
    """
    
    result = ""
    for variable in variables:
        v = query_variables(variable)
        result += "&nvars=" + str(v) 
        
    return result

