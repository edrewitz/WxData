"""
This file hosts historical and forecast data for the various climate models:

1) CMCC-CM2-VHR4 - Italy - Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici, Lecce (CMCC) - 30 km
2) FGOALS_f3_H - China - Chinese Academy of Sciences, Beijing (CAS) - 28 km
3) HiRAM_SIT_HR - Taiwan - Research Center for Environmental Changes, Academia Sinica, Nankang, Taipei (AS-RCEC) - 25 km
4) MRI_AGCM3_2_S - Japan - Meteorological Research Institute, Tsukuba, Ibaraki (MRI) - 20 km
5) EC_Earth3P_HR - Europe - EC-Earth consortium, Rossby Center, Swedish Meteorological and Hydrological Institute/SMHI, Norrkoping, Sweden - 29 km
6) MPI_ESM1_2_XR - Germany - Max Planck Institute for Meteorology, Hamburg 20146, Germany - 51 km
7) NICAM16_8S - Japan - Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan (MIROC) - 31 km

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import pandas as _pd
from wxdata.utils.api import(
    json_to_pandas as _json_to_pandas,
    server_response as _server_response,
    df_to_csv as _df_to_csv
)

def cmcc_cm2_vhr4(latitude,
            longitude,
            start_date='1950-01-01',
            end_date='2050-12-31',
            temperature_units='fahrenheit',
            wind_speed_units='mph',
            precipitation_units='inch',
            variables=['temperature_2m_max',
                        'temperature_2m_mean',
                        'temperature_2m_min',
                        'wind_speed_10m_mean',
                        'wind_speed_10m_max',
                        'relative_humidity_2m_mean',
                        'relative_humidity_2m_max',
                        'relative_humidity_2m_min',
                        'dew_point_2m_mean',
                        'dew_point_2m_min',
                        'dew_point_2m_max',
                        'precipitation_sum'],
            proxies=None,
            to_csv=False,
            path=f"Open Meteo Data/Climate/CMCC-CM2-VHR4",
            filename=f"CMCC-CM2-VHR4.csv"):
    
    """
    This function retrieves daily CMCC-CM2-VHR4 climate data from the Open-Meteo API for a given point of latitude/longitude.
    
    Required Arguments:
    
    1) latitude (Float or Integer) - Latitude in decimal degrees.
    
    2) longitude (Float or Integer) - Longitude in decimal degrees.
    
    Optional Arguments:
    
    1) start_date (String) - Default='1950-01-01'. Start date in the format of 'YYYY-mm-dd'. Record begins at 1950-01-01.
    
    2) end_date (String) - Default='2050-12-31'. End date in the format of 'YYYY-mm-dd'. Record ends at 2050-12-31.
    
    3) temperature_units (String) - Default='fahrenheit'. The units for temperature.
    
        Valid Temperature Units
        -----------------------
        
        1) fahrenheit
        2) celsius
        
    4) wind_speed_units (String) - Default='mph'. The units for wind speed. 
    
        Valid Wind Speed Units
        ----------------------
        
        1) mph - miles per hour
        2) kmh - kilometers per hour
        3) ms - meters per second
        4) kn - knots
        
    5) precipitation_units (String) - Default='inch'. The units for precipitation amounts.
    
        Valid Precipitation Units
        -------------------------
        
        1) inch - inches
        2) mm - millimeters
        
    6) variables (String List) - Default=['temperature_2m_max',
                                            'temperature_2m_mean',
                                            'temperature_2m_min',
                                            'wind_speed_10m_mean',
                                            'wind_speed_10m_max',
                                            'relative_humidity_2m_mean',
                                            'relative_humidity_2m_max',
                                            'relative_humidity_2m_min',
                                            'dew_point_2m_mean',
                                            'dew_point_2m_min',
                                            'dew_point_2m_max',
                                            'precipitation_sum']
   
                                            
                The list of variables to choose from.
                
    7) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    8) to_csv (Boolean) - Default=False. When set to True the data will be saved as a CSV file to {path} with {filename}
    
    9) path (String) - The path where the CSV file is saved to.
    
    10) filename (String) - The filename for the CSV file.                     
                    
    Returns
    -------
    
    A Pandas.DataFrame of the CMCC-CM2-VHR4 time series for point latitude/longitude. 
    """
    
    if proxies == None:
        response = _requests.get(f"https://climate-api.open-meteo.com/v1/climate?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&start_date={start_date}&end_date={end_date}"
                             f"&daily={','.join(variables)}&models=CMCC_CM2_VHR4"
                             f"&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}")
        
        
        
    else:
        response = _requests.get(f"https://climate-api.open-meteo.com/v1/climate?"
                             f"latitude={latitude}&longitude={longitude}"
                             f"&start_date={start_date}&end_date={end_date}"
                             f"&daily={','.join(variables)}&models=CMCC_CM2_VHR4"
                             f"&wind_speed_unit={wind_speed_units}"
                             f"&precipitation_unit={precipitation_units}&temperature_unit={temperature_units}",
                             proxies=proxies)
        
    _server_response(response)
        
    data = response.json()
    
    df = _json_to_pandas(data,
                         field='daily')
    
    df['time'] = _pd.to_datetime(df['time'])
        
    if to_csv == True:
        _df_to_csv(df,
                   path,
                   filename)
    
    return df