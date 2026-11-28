"""
This file hosts the interface to retrieve a single station timeseries of observational data from MADIS

(C) Eric J. Drewitz 2025-2026
"""
import requests as _requests
import sys as _sys
import pandas as _pd
import os as _os
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.observational_data.madis.exceptions import request_error as _request_error
from wxdata.observational_data.madis.variables import url_variables as _url_variables
from wxdata.observational_data.madis.qc_levels import qc_level as _qc_level
from wxdata.observational_data.madis.dataframe import(
    clean_data as _clean_data,
    convert_temperature as _convert_temperature
)
from bs4 import BeautifulSoup as _BeautifulSoup
from io import StringIO as _StringIO
from time import sleep as _sleep

try:
    from datetime import(
        datetime as _datetime, 
        timedelta as _timedelta, 
        UTC as _UTC
    )
except Exception as e:
    from datetime import(
        datetime as _datetime, 
        timedelta as _timedelta
    )

try:
    now = _datetime.now(_UTC)
except Exception as e:
    now = _datetime.utcnow()

def _observation_times(start_time,
                       end_time,
                       interval,
                       interval_units):
    
    """
    This function creates a list of times for our single station timeseries dataset request.
    
    Required Arguments:
    
    1) start_time (String or datetime) - The start time for the request. If user enters as a string, must be in 'YYYY-mm-dd HH:MM' format.
    
    2) end_time (String or datetime) - The end time for the request. If user enters as a string, must be in 'YYYY-mm-dd HH:MM' format.
    
    3) interval (String) - The time interval (i.e. 10 for every 10 minutes)
    
    4) interval_units (String) - The units in time for the interval (minutes, hours or days)
    
    Optional Arguments: None
    
    **Returns**
    
    A list of times for our request
    """
    
    if type(start_time) == type(now):
        pass
    else:
        start_time = _datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    
    if type(end_time) == type(now):
        pass
    else:
        end_time = _datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        
    time_units = ["days", "hours", "minutes"]
    
    if interval_units not in time_units:
        print(f"{interval_units} is not a valid interval unit.")
        print(f"Valid Interval Units: 'minutes', 'hours' or 'days'.")
        print(f"Please try again.\nSystem Exit.")
        _sys.exit(1)
    else:
        pass
    
    if interval_units == 'minutes':
        times = []
        current = start_time
        step = _timedelta(minutes=interval)
        while current <= end_time: 
            times.append(current)
            current += step
            
    elif interval_units == 'hours':
        times = []
        current = start_time
        step = _timedelta(hours=interval)
        while current <= end_time: 
            times.append(current)
            current += step
            
    else:
        times = []
        current = start_time
        step = _timedelta(days=interval)
        while current <= end_time: 
            times.append(current)
            current += step
            
    return times
    

def madis_single_station_timeseries(station_id,
                                    start_time,
                                    end_time,
                                    interval=5,
                                    interval_units='minutes',
                                    variables=['dew point temperature',
                                               'relative humidity',
                                               'temperature',
                                               'wind direction',
                                               'wind speed',
                                               'altimeter'],
                                    qc_level='return observations passing all quality control checks',
                                    proxies=None,
                                    to_csv=False,
                                    path='MADIS Data/Single Station Timeseries',
                                    filename='default',
                                    return_pandas_df=True,
                                    convert_temperature=True,
                                    convert_to='fahrenheit',
                                    notifications="on"):
    
    """
    This function downloads single station time series observations from the NOAA MADIS API and returns a Pandas.DataFrame of this data.
    
    Required Arguments:
    
    1) station_id (String) - The station identifier.
    
    2) start_time (String or datetime) - The start time for the request. If user enters as a string, must be in 'YYYY-mm-dd HH:MM' format.
    
    3) end_time (String or datetime) - The end time for the request. If user enters as a string, must be in 'YYYY-mm-dd HH:MM' format.
    
    Optional Arguments:
    
    1) interval (String) - Default=5. The time interval (i.e. 10 for every 10 minutes).
        This is specific to ASOS stations. For non-ASOS stations, this may need to be changed as 
        non-ASOS stations report in different intervals (i.e. 10 minute observations)
    
    2) interval_units (String) - Default='minutes'. The units in time for the interval (minutes, hours or days).
    
    3) variables (String List) - Default=['dew point temperature',
                                               'relative humidity',
                                               'temperature',
                                               'wind direction',
                                               'wind speed',
                                               'altimeter']
        
        ***Important***: Not every variable is available at every station.
                                               
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
        
    4) qc_level (String) - Default='return observations passing all quality control checks'.
    
        This represents the level of quality control checks for an observation. The default is the highest level
        of QC checks.
    
        ***QC Check Levels***
        
        'return all observations regardless of quality control results'
        'return observations passing level 1'
        'return observations passing levels 1 and 2'
        'return observations passing levels 1 through 3'
        'return observations passing all quality control checks'

        QC Flags (As seen in the returned Pandas.DataFrame)
        V	- Verified: Passed all three QC levels.
        C - Coarse pass: Passed Level 1 (validity), meaning it is physically plausible, though higher-level spatial/temporal checks were not applied or passed.
        Z	- Preliminary/No QC: No QC checks performed.

    5) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    6) to_csv (Boolean) - Default=False. Set to True to create a CSV file of the data.
    
    7) path (String) - Default='MADIS Data/Single Station Timeseries'. The parent directory for the MADIS data.
    
    8) filename (String) - Default='default'. When set to 'default' the filename convention is as follows:
    
        `filename = {STATION_ID}-{START_TIME}-{END_TIME}.csv`
        
        Change 'default' to 'custom_file_name.csv' for manual file naming. 
        
    9) return_pandas_df (Boolean) - Default=True. When set to True, a Pandas.DataFrame is returned to the user.
        The case where you may want to set `return_pandas_df=False` is when `to_csv=True` as you will be creating a 
        CSV file of the data.
        
    10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    11) convert_to (String) - Default='fahrenheit'. When set to 'fahrenheit' temperature related fields convert to Fahrenheit.
        Set convert_to='celsius' for Celsius. 
        
    12) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
        
    **Returns**
    
    A Pandas.DataFrame of the cleaned up Single Station Time Series MADIS Data
    
                        OR
                        
    A CSV file of the cleaned up Single Station Time Series MADIS Data.
    
    """
    
    station_id = station_id.upper()
    
    times = _observation_times(start_time,
                                end_time,
                                interval,
                                interval_units)
    
    qc_checks = _qc_level(qc_level)
    url_variables = _url_variables(variables)
    
    df_list = []
    
    for t in times:
        if proxies == None:
            response = _requests.get(f"https://madis-data.ncep.noaa.gov/madisPublic/cgi-bin/madisXmlPublicDir?"
                                     f"rdr=&time={t.strftime('%Y%m%d_%H%M')}&minbck=0&minfwd=0&recwin=3&timefilter=0&dfltrsel=3&"
                                     f"state=CA&latll=0.0&lonll=0.0&latur=90.0&lonur=0.0&stanam={station_id}&stasel=1&"
                                     f"pvdrsel=0&varsel=1&qctype=0&qcsel={qc_checks}&xml=5&csvmiss=0&"
                                     f"{url_variables}")
            
            if response.status_code != 200:
                for i in range(0, 10, 1):
                    _sleep(60)
                    response = _requests.get(f"https://madis-data.ncep.noaa.gov/madisPublic/cgi-bin/madisXmlPublicDir?"
                                            f"rdr=&time={t.strftime('%Y%m%d_%H%M')}&minbck=0&minfwd=0&recwin=3&timefilter=0&dfltrsel=3&"
                                            f"state=CA&latll=0.0&lonll=0.0&latur=90.0&lonur=0.0&stanam={station_id}&stasel=1&"
                                            f"pvdrsel=0&varsel=1&qctype=0&qcsel={qc_checks}&xml=5&csvmiss=0&"
                                            f"{url_variables}")
                    if response.status_code == 200:
                        break
                    else:
                        i = i
                        if i >= 9:
                            _request_error(response)
        else:
            response = _requests.get(f"https://madis-data.ncep.noaa.gov/madisPublic/cgi-bin/madisXmlPublicDir?"
                                     f"rdr=&time={t.strftime('%Y%m%d_%H%M')}&minbck=0&minfwd=0&recwin=3&timefilter=0&dfltrsel=3&"
                                     f"state=CA&latll=0.0&lonll=0.0&latur=90.0&lonur=0.0&stanam={station_id}&stasel=1&"
                                     f"pvdrsel=0&varsel=1&qctype=0&qcsel={qc_checks}&xml=5&csvmiss=0&"
                                     f"{url_variables}",
                                    proxies=proxies)
            
            if response.status_code != 200:
                for i in range(0, 10, 1):
                    _sleep(60)
                    response = _requests.get(f"https://madis-data.ncep.noaa.gov/madisPublic/cgi-bin/madisXmlPublicDir?"
                                            f"rdr=&time={t.strftime('%Y%m%d_%H%M')}&minbck=0&minfwd=0&recwin=3&timefilter=0&dfltrsel=3&"
                                            f"state=CA&latll=0.0&lonll=0.0&latur=90.0&lonur=0.0&stanam={station_id}&stasel=1&"
                                            f"pvdrsel=0&varsel=1&qctype=0&qcsel={qc_checks}&xml=5&csvmiss=0&"
                                            f"{url_variables}",
                                            proxies=proxies)
                    if response.status_code == 200:
                        break
                    else:
                        i = i
                        if i >= 9:
                            _request_error(response)
                
        soup = _BeautifulSoup(response.content, "html.parser")
        data = _StringIO(soup.find_all('pre')[0].contents[0])
        df = _pd.read_csv(data)
        df_list.append(df)
        
    df = _pd.concat(df_list)
    
    df = _clean_data(df)
    
    if convert_temperature == True:
        df = _convert_temperature(df,
                                  convert_to)
    else:
        pass
    
    if to_csv == True:
        _os.makedirs(path, exist_ok=True)
        
        if filename == 'default':
            if type(start_time) == type(now) and type(end_time) == type(now):
                filename = f"{station_id}-{start_time.strftime('%Y-%m-%d-%H%M')}-{end_time.strftime('%Y-%m-%d-%H%M')}.csv"
            else:
                start_time = start_time.replace(' ', '-')
                start_time = start_time.replace(':', '')
                
                end_time = end_time.replace(' ', '-')
                end_time = end_time.replace(':', '')
                
                filename = f"{station_id}-{start_time}-{end_time}.csv"
        else:
            filename = filename
            
        df.to_csv(f"{path}/{filename}", index=False)
        if notifications == "on":
            print(f"{filename} saved to {path}")
        else:
            pass
    else:
        pass
    
    if return_pandas_df == True:
        return df
    else:
        pass

    