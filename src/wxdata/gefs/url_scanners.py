"""
This file hosts the GEFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import numpy as np
import time

from urllib.parse import urlparse, parse_qs
from wxdata.utils.coords import convert_lon
from wxdata.gefs.exception_messages import(
    
    gefs0p50,
    gefs0p25
)

from wxdata.utils.nomads_gribfilter import(
    
    result_string,
    key_list
)

# Exception handling for Python >= 3.13 and Python < 3.13
try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

# Gets current time in UTC
try:
    now = datetime.now(UTC)
except Exception as e:
    now = datetime.utcnow()

# Gets local time
local = datetime.now()

# Gets yesterday's date
yd = now - timedelta(days=1)

NCEP_NOMADS_PREFIX = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/gens/prod/"
AMAZON_AWS_PREFIX = f"https://noaa-gefs-pds.s3.amazonaws.com/"
GOOGLE_CLOUD_PREFIX = f"https://storage.googleapis.com/gfs-ensemble-forecast-system/"

def gefs_0p50_url_scanner(cat, 
                          final_forecast_hour, 
                          proxies, 
                          members,
                          source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - The northern bound of the data needed.

    6) southern_bound (Float or Integer) - The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    10) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.     
    """
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
            
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'mean':
        aa = f"avg"
    # Ensemble Members
    elif cat == 'members':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # Ensemble Spread
    elif cat == 'spread':
        aa = f"spr"
    # User enters an invalid category
    # When a category is invalid - Defaults to Ensemble Mean
    else:
        gefs0p50.gefs0p50_cat_error('gefs0p50')
        aa = f"avg"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        gefs0p50.forecast_hour_error()
        final_forecast_hour = 384
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2ap5/")
    today_12z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2ap5/")
    today_06z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2ap5/")
    today_00z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2ap5/")
    
    yesterday_18z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2ap5/")
    yesterday_12z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2ap5/")
    yesterday_06z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2ap5/")
    yesterday_00z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2ap5/")
        
    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2a.0p50.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2a.0p50.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2a.0p50.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2a.0p50.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i     
    
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i  
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z_scan,
        today_12z_scan,
        today_06z_scan,
        today_00z_scan,
        yesterday_18z_scan,
        yesterday_12z_scan,
        yesterday_06z_scan,
        yesterday_00z_scan
    ]
    
    responses = [
        t_18,
        t_12,
        t_06,
        t_00,
        y_18,
        y_12,
        y_06,
        y_00
    ]
    
    filenames = [
        f_18z,
        f_12z,
        f_06z,
        f_00z,
        f_18z,
        f_12z,
        f_06z,
        f_00z
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url, filename in zip(responses, urls, filenames):
        if response.status_code == 200:
            url = url
            run = int(f"{url[-18]}{url[-17]}")
            filename = filename
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    return url, filename, run


def gefs_0p50_secondary_parameters_url_scanner(cat, 
                                                final_forecast_hour, 
                                                proxies, 
                                                members,
                                                source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) control
    4) spread
    
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P50 SECONDARY PARAMETERS
    goes out to 384 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    384 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - The northern bound of the data needed.

    6) southern_bound (Float or Integer) - The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    10) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P50 SECONDARY PARAMETERS
        ----------------------------------------------------
        
        'best lifted index'
        '5 wave geopotential height'
        'absolute vorticity'
        'temperature'
        'dew point'
        'convective precipitation'
        'albedo'
        'apparent temperature'
        'brightness temperature'
        'convective available potential energy'
        'clear sky uv-b downward solar flux'
        'convective inhibition'
        'cloud mixing ratio'
        'plant canopy surface water'
        'percent frozen precipitaion'
        'convective precipitation rate'
        'cloud water'
        'cloud work function'
        'uv-b downward solar flux'
        'field capacity'
        'surface friction velocity'
        'ground heat flux'
        'wind gust'
        'geopotential height'
        'haines index'
        'storm relative helicity'
        'planetary boundary layer height'
        'icao standard atmosphere reference height'
        'ice cover'
        'icing'
        'icing severity'
        'land cover'
        'surface lifted index'
        'montgomery stream function'
        'mslp (eta model reduction)'
        'large scale non-convective precipitation'
        'ozone mixing ratio'
        'potential evaporation rate'
        'parcel lifted index (to 500mb)'
        'pressure level from which parcel was lifted'
        'potential temperature'
        'precipitation rate'
        'pressure'
        'potential vorticity'
        'precipitable water'
        'relative humidity'
        'surface roughness'
        'snow phase-change heat flux'
        'snow cover'
        'liquid volumetric soil moisture (non-frozen)'
        'volumetric soil moisture content'
        'specific humidity'
        'sunshine duration'
        'total cloud cover'
        'total ozone'
        'soil temperature'
        'momentum flux (u-component)'
        'u-component of wind'
        'zonal flux of gravity wave stress'
        'u-component of storm motion'
        'upward shortwave radiation flux'
        'momentum flux (v-component)'
        'v-component of wind'
        'meridional flux of gravity wave stress'
        'visibility'
        'ventilation rate'
        'v-component of storm motion'
        'vertical velocity'
        'vertical speed shear'
        'water runoff'
        'wilting point'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.        
    """
    cat = cat.lower()
    
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
    
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'members' or cat == 'mean' or cat == 'spread':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # User enters an invalid category
    # When a category is invalid - Defaults to Control Run
    else:
        gefs0p50.gefs0p50_cat_error('gefs0p50 secondary parameters')
        aa = f"c00"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 384:
        gefs0p50.forecast_hour_error()
        final_forecast_hour = 384
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    
    today_18z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2bp5/")
    today_12z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2bp5/")
    today_06z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2bp5/")
    today_00z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2bp5/")
    
    yesterday_18z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2bp5/")
    yesterday_12z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2bp5/")
    yesterday_06z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2bp5/")
    yesterday_00z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2bp5/")
        
    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2b.0p50.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2b.0p50.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2b.0p50.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2b.0p50.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i     
    
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i         
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z_scan,
        today_12z_scan,
        today_06z_scan,
        today_00z_scan,
        yesterday_18z_scan,
        yesterday_12z_scan,
        yesterday_06z_scan,
        yesterday_00z_scan
    ]
    
    responses = [
        t_18,
        t_12,
        t_06,
        t_00,
        y_18,
        y_12,
        y_06,
        y_00
    ]
    
    filenames = [
        f_18z,
        f_12z,
        f_06z,
        f_00z,
        f_18z,
        f_12z,
        f_06z,
        f_00z
    ]
    
    # Testing the status code and then returning the first link with a status code of 200
    for response, url, filename in zip(responses, urls, filenames):
        if response.status_code == 200:
            url = url
            filename = filename
            run = int(f"{url[-18]}{url[-17]}")
            break      
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    

    
    return url, filename, run
            

def gefs_0p25_url_scanner(cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        source):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) cat (string) - The category of the ensemble data. 
    
    Valid categories
    -----------------
    
    1) mean
    2) members
    3) spread
    4) control
    
    2) final_forecast_hour (Integer) - The final forecast hour the user wishes to download. The GEFS0P25
    goes out to 240 hours. For those who wish to have a shorter dataset, they may set final_forecast_hour to a value lower than 
    240 by the nereast increment of 3 hours. 
    
    3) western_bound (Float or Integer) - The western bound of the data needed. 

    4) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    5) northern_bound (Float or Integer) - The northern bound of the data needed.

    6) southern_bound (Float or Integer) - The southern bound of the data needed.

    7) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    8) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    9) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    10) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for GEFS0P25
        -------------------------------
        
			'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'categorical rain'
            'categorical snow'
            'convective inhibition'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'geopotential height'
            'ice thickness'
            'latent heat net flux'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'sensible heat net flux'
            'snow depth'
            'volumetric soil moisture content'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'soil temperature'
            'u-component of wind'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'v-component of wind'
            'vertical velocity'
            'water equivalent of accumulated snow depth'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.    
    """
    cat = cat.lower()
    
    source = source.lower()
    if source == 'noaa':
        PREFIX = NCEP_NOMADS_PREFIX
    elif source == 'aws':
        PREFIX = AMAZON_AWS_PREFIX
    else:
        PREFIX = GOOGLE_CLOUD_PREFIX
    
    m = []
    for member in members:
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"      
        
        m.append(aa) 
    
    # Gets the file abbreviation based on category
    # Ensemble Mean
    if cat == 'mean':
        aa = f"avg"
    # Ensemble Members
    elif cat == 'members':
        member = members[-1]
        if member < 10:
            aa = f"p0{member}"
        else:
            aa = f"p{member}"
    # Control Run
    elif cat == 'control':
        aa = f"c00"
    # Ensemble Spread
    elif cat == 'spread':
        aa = f"spr"
    # User enters an invalid category
    # When a category is invalid - Defaults to Ensemble Mean
    else:
        gefs0p25.gefs0p25_cat_error()
        aa = f"avg"
        
    # This section handles the final forecast hour for the filename
    if final_forecast_hour > 240:
        gefs0p25.forecast_hour_error()
        final_forecast_hour = 240
    else:
        final_forecast_hour = final_forecast_hour
        
    if final_forecast_hour >= 100:
        final_forecast_hour = f"{final_forecast_hour}"
    elif final_forecast_hour >= 10 and final_forecast_hour < 100:
        final_forecast_hour = f"0{final_forecast_hour}"
    else:
        final_forecast_hour = f"00{final_forecast_hour}"
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/")
    today_12z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/")
    today_06z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/")
    today_00z_scan = (f"{PREFIX}gefs.{now.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/")
    
    yesterday_18z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/18/atmos/pgrb2sp25/")
    yesterday_12z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/12/atmos/pgrb2sp25/")
    yesterday_06z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/06/atmos/pgrb2sp25/")
    yesterday_00z_scan = (f"{PREFIX}gefs.{yd.strftime('%Y%m%d')}/00/atmos/pgrb2sp25/")
    
    # The filenames for the different run times
    f_18z = f"ge{aa}.t18z.pgrb2s.0p25.f{final_forecast_hour}"
    f_12z = f"ge{aa}.t12z.pgrb2s.0p25.f{final_forecast_hour}"
    f_06z = f"ge{aa}.t06z.pgrb2s.0p25.f{final_forecast_hour}"
    f_00z = f"ge{aa}.t00z.pgrb2s.0p25.f{final_forecast_hour}"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i     
    
    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                stream=True, 
                                proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                stream=True, 
                                proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                stream=True, 
                                proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                stream=True, 
                                proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 10, 1):
                time.sleep(30)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", 
                                        stream=True, 
                                        proxies=proxies)
                    y_00.close()   
                    break
                except Exception as e:
                    i = i  
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z_scan,
        today_12z_scan,
        today_06z_scan,
        today_00z_scan,
        yesterday_18z_scan,
        yesterday_12z_scan,
        yesterday_06z_scan,
        yesterday_00z_scan
    ]
    
    responses = [
        t_18,
        t_12,
        t_06,
        t_00,
        y_18,
        y_12,
        y_06,
        y_00
    ]
    
    filenames = [
        f_18z,
        f_12z,
        f_06z,
        f_00z,
        f_18z,
        f_12z,
        f_06z,
        f_00z
    ]
    
    # Testing the status code and then returning the first link with a status code of 200

    for response, url, filename in zip(responses, urls, filenames):
        if response.status_code == 200:
            url = url
            filename = filename
            run = int(f"{url[-19]}{url[-18]}")
            break      
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    

    return url, filename, run