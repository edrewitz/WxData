"""
This file has all the functions to construct the Pandas.DataFrame of the MADIS data.

(C) Eric J. Drewitz 2025-2026
"""
import pandas as pd
import numpy as np

def convert_temperature(df,
                        convert_to):
    
    """
    Converts from Kelvin to Celsius or Fahrenheit.
    
    Required Arguments:
    
    1) df (Pandas.DataFrame) - The Pandas.DataFrame
    
    2) convert_to (String) - The units to convert to (celsius or fahrenheit).
    
    **Returns**
    
    All temperature related fields are converted to the proper units    
    """
    
    keyword_1 = "temperature"
    keyword_2 = "dew point"
    params = list(df.columns)
    for param in params:
        if keyword_1 in param or keyword_2 in param:
            if convert_to == 'celsius':
                try:
                    df[param] = df[param] - 273.15
                except Exception as e:
                    pass
            else:
                try:
                    df[param] = df[param] - 273.15
                    df[param] = (df[param] * (9/5)) + 32
                except Exception as e:
                    pass
                
    return df
    
def clean_data(df):
    
    """
    This function reformats our Pandas.DataFrame to clean up headers and missing data. 
    
    Required Arguments:
    
    1) Pandas.DataFrame of the data
    
    Optional Arguments: None
    
    **Returns**
    
    A cleaned Pandas.DataFrame more readable to the user.  
    """
    
    col_headers = {
        
        'station id':'STAID',
        'observation date':'OBDATE',
        'observation time':'OBTIME',
        'data provider':'PVDR',
        'data sub-provider':'SUBPVDR',
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
        'time of 24-hour minimum temperature':'T24MINT',
        'time of 24-hour maximum temperature':'T24MAXT',
        'first observation time in 15 minute period':'FOT15M',
        'last observation time in 15 minute period':'LOT15M',
        'raw metar message':'RAWMTR'
    }

    df.columns = df.columns.astype(str).str.strip()

    reverse_headers = {
        value: key
        for key, value in col_headers.items()
    }

    df = df.rename(columns=reverse_headers)

    new_columns = []

    for i, col in enumerate(df.columns):

        if col == "D" or str(col).startswith("D."):

            if i > 0:

                previous_col = new_columns[-1]

                if not previous_col.endswith("qc flag"):
                    new_columns.append(
                        f"{previous_col} qc flag"
                    )
                else:
                    new_columns.append(col)

            else:
                new_columns.append("qc flag")

        else:
            new_columns.append(col)

    df.columns = new_columns

    missing_values = [
        -99,
        -999,
        -9999,
        -99999,
        -999999
    ]

    df = df.replace(missing_values, np.nan)

    df = df.dropna(axis=1, how="all")

    df = df.drop(
        columns=[
            col
            for col in df.columns
            if (
                col.endswith(" qc flag")
                and col.removesuffix(" qc flag") not in df.columns
            )
        ],
        errors="ignore"
    )

    ordered_cols = [
        col
        for col in col_headers.keys()
        if col in df.columns
    ]

    extra_cols = [
        col
        for col in df.columns
        if col not in ordered_cols
    ]

    df = df[ordered_cols + extra_cols]
    
    for col in df.columns:

        # Skip date/time columns
        if "date" in col.lower() or "time" in col.lower():
            continue

        if df[col].dtype == object:

            converted = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            original_non_null = df[col].notna().sum()
            converted_non_null = converted.notna().sum()

            # Convert only if all non-null values are numeric
            if (
                original_non_null > 0
                and converted_non_null == original_non_null
            ):
                df[col] = converted.astype(float)
    
    return df
