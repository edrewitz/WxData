"""
This file hosts the CFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import os
import time
import warnings 
warnings.filterwarnings('ignore')

from wxdata.utils.coords import convert_lon
from bs4 import BeautifulSoup
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

def forecast_file_times(cat,
                        proxies,
                        final_forecast_hour):
    
    """
    This function returns the datetimes for the following:
    
    1) Final Forecast File
    2) Model Initialization
    
    Required Arguments:
    
    1) cat (String) - The category of CFS data.
    
    Categories
    ----------
    
    1) flux
    2) pressure
    
    2) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    3) final_forecast_hour (Integer) - The last forecast hour of the query. For performance reasons, it is recommended
        to not download the entire set of CFS 6 hourly data. 
    
    Returns
    -------
    
    The datetimes of the final forecast file and model initialization in string format.    
    """
    
    cat = cat.lower()
    
    if cat == 'flux':
        cat = 'flxf'
    else:
        cat = 'pgbf'
    
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/18/6hrly_grib_01/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/12/6hrly_grib_01/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/06/6hrly_grib_01/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/00/6hrly_grib_01/")

    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01/")

    urls = []
    urls.append(today_18z_scan)
    urls.append(today_12z_scan)
    urls.append(today_06z_scan)
    urls.append(today_00z_scan)
    urls.append(yesterday_18z_scan)
    urls.append(yesterday_12z_scan)
    urls.append(yesterday_06z_scan)
    urls.append(yesterday_00z_scan)
    
    for url in urls:    
        if proxies==None:  
            try:
                response = requests.get(url, stream=True)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url, stream=True)
                        break
                    except Exception as e:
                        i = i
                        
        else:
            try:
                response = requests.get(url, stream=True, proxies=proxies)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url, stream=True, proxies=proxies)
                        break
                    except Exception as e:
                        i = i
        if response.status_code == 200:
            html_content = response.text
            break
        else:
            pass   
        
    response.close()
    soup = BeautifulSoup(html_content, 'html.parser')
    file_names = set() 
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '.' in href and not href.startswith('#') and not href.startswith('mailto:'):
            filename = os.path.basename(href)
            file_names.add(filename)
                
        marker = ".idx"
        fnames = []
        for filename in sorted(list(file_names)):
            if marker not in filename:
                fnames.append(filename)
        
        files = []
        for f in fnames:
            if cat in f:
                files.append(f)

    file_index = (final_forecast_hour/6)
    if len(files) < (file_index + 1):
        if now.day == local.day:
            origional = int(f"{url[-17]}{url[-16]}")
            corrected = origional - 6
            if corrected == 0:
                corrected = '00'
            elif corrected == 6:
                corrected = '06'
            else:
                corrected = str(corrected)
            new_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/{corrected}/6hrly_grib_01/"

            if proxies==None:  
                try:
                    response = requests.get(new_url, stream=True)
                except Exception as e:
                    for i in range(0, 10, 1):
                        time.sleep(60)
                        try:
                            response = requests.get(new_url, stream=True)
                            break
                        except Exception as e:
                            i = i
                        
            else:
                try:
                    response = requests.get(new_url, stream=True, proxies=proxies)
                except Exception as e:
                    for i in range(0, 10, 1):
                        time.sleep(60)
                        try:
                            response = requests.get(new_url, stream=True, proxies=proxies)
                            break
                        except Exception as e:
                            i = i
            if response.status_code == 200:
                html_content = response.text
            else:
                pass   
            
            response.close()
            soup = BeautifulSoup(html_content, 'html.parser')
            file_names = set() 
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '.' in href and not href.startswith('#') and not href.startswith('mailto:'):
                    filename = os.path.basename(href)
                    file_names.add(filename)
                        
                marker = ".idx"
                fnames = []
                for filename in sorted(list(file_names)):
                    if marker not in filename:
                        fnames.append(filename)
                
                files = []
                for f in fnames:
                    if cat in f:
                        files.append(f)
                        
        else:
            yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01/")
            yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01/")
            yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01/")
            yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01/")
        
            urls = []
            urls.append(yesterday_18z_scan)
            urls.append(yesterday_12z_scan)
            urls.append(yesterday_06z_scan)
            urls.append(yesterday_00z_scan)
            
            for url in urls:    
                if proxies==None:  
                    try:
                        response = requests.get(url, stream=True)
                    except Exception as e:
                        for i in range(0, 10, 1):
                            time.sleep(60)
                            try:
                                response = requests.get(url, stream=True)
                                break
                            except Exception as e:
                                i = i
                else:
                    try:
                        response = requests.get(url, stream=True, proxies=proxies)
                    except Exception as e:
                        for i in range(0, 10, 1):
                            time.sleep(60)
                            try:
                                response = requests.get(url, stream=True, proxies=proxies)
                                break
                            except Exception as e:
                                i = i
                if response.status_code == 200:
                    html_content = response.text
                    break
                else:
                    pass   
                
            response.close()
            soup = BeautifulSoup(html_content, 'html.parser')
            file_names = set() 
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '.' in href and not href.startswith('#') and not href.startswith('mailto:'):
                    filename = os.path.basename(href)
                    file_names.add(filename)
                        
                marker = ".idx"
                fnames = []
                for filename in sorted(list(file_names)):
                    if marker not in filename:
                        fnames.append(filename)
                
                files = []
                for f in fnames:
                    if cat in f:
                        files.append(f)
                        

            if len(files) < (file_index + 1):
                origional = int(f"{url[-17]}{url[-16]}")
                corrected = origional - 6
                if corrected == 0:
                    corrected = '00'
                elif corrected == 6:
                    corrected = '06'
                else:
                    corrected = str(corrected)
                new_url = f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/{corrected}/6hrly_grib_01/"
    
                if proxies==None:  
                    try:
                        response = requests.get(new_url, stream=True)
                    except Exception as e:
                        for i in range(0, 10, 1):
                            time.sleep(60)
                            try:
                                response = requests.get(new_url, stream=True)
                                break
                            except Exception as e:
                                i = i
                else:
                    try:
                        response = requests.get(new_url, stream=True, proxies=proxies)
                    except Exception as e:
                        for i in range(0, 10, 1):
                            time.sleep(60)
                            try:
                                response = requests.get(new_url, stream=True, proxies=proxies)
                                break
                            except Exception as e:
                                i = i
                if response.status_code == 200:
                    html_content = response.text
                else:
                    pass   
                
                response.close()
                soup = BeautifulSoup(html_content, 'html.parser')
                file_names = set() 
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if '.' in href and not href.startswith('#') and not href.startswith('mailto:'):
                        filename = os.path.basename(href)
                        file_names.add(filename)
                            
                    marker = ".idx"
                    fnames = []
                    for filename in sorted(list(file_names)):
                        if marker not in filename:
                            fnames.append(filename)
                    
                    files = []
                    for f in fnames:
                        if cat in f:
                            files.append(f)
                            
                
    
    initial = files[0]
    init_date = f"{initial[4:14]}"
    runtime = f"{initial[18:28]}"
    init = f"{runtime[0:8]}"
    date = datetime.strptime(init_date, '%Y%m%d%H')
    date = date + timedelta(hours=final_forecast_hour)
    final = f"{cat}{date.strftime('%Y%m%d%H')}.01.{runtime}.grb2"
    idx = files.index(final)
    files = files[0:(idx + 1)]
            
    date = f"{date.strftime('%Y%m%d%H')}"
    
    return date, init, files

def cfs_flux_url_scanner(western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          variables,
                          final_forecast_hour):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) western_bound (Float or Integer) - The western bound of the data needed. 

    2) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    3) northern_bound (Float or Integer) - The northern bound of the data needed.

    4) southern_bound (Float or Integer) - The southern bound of the data needed.

   5) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                                
    6) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for CFS Flux
        -------------------------------
        
			'aerodynamic conductance'
            'albedo'
            'clear sky uv-b downward solar flux'
            'plant canopy surface water'
            'convective precipitation rate'
            'categorical rain'
            'clear sky downward longwave flux'
            'clear sky downward solar flux (surface)'
            'clear sky downward solar flux (top of the atmosphere)'
            'clear sky upward solar flux'
            'cloud work function'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'clear sky uv-b downward solar flux'
            'direct evaporation from bare soil'
            'canopy water evaporation'
            'surface friction velocity'
            'ground heat flux'
            'geopotential height'
            'planetary boundary layer height'
            'ice cover'
            'ice thickness'
            'land cover'
            'latent heat net flux'
            'near ir beam downward solar flux'
            'near ir diffuse downward solar flux'
            'potential evaporation rate'
            'precipitation rate'
            'pressure'
            'precipitable water'
            '2-meter maximum specific humidity'
            '2-meter minimum specific humidity'
            'sublimation (evaporation from snow)'
            'surface roughness'
            'sedimentation mass flux'
            'sensible heat net flux'
            'surface slope type'
            'snow depth'
            'snow phase-change heat flux'
            'snow cover'
            'liquid volumetric soil moisture (non-frozen)'
            'soil moisture content'
            'volumetric soil moisture content'
            'soil type'
            'specific humidity'
            'snowfall rate water equivalent'
            'storm surface runoff (non-infiltrating)'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'transpiration'
            'momentum flux (u-component)'
            'u-component of wind'
            'zonal flux of gravity wave stress'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'visible beam downward solar flux'
            'vegetation'
            'momentum flux (v-component)'
            'v-component of wind'
            'vegetation type'
            'meridional flux of gravity wave stress'
            'water runoff'
            'water equivalent of accumulated snow depth'
            
    7) final_forecast_hour (Integer) - The last forecast hour of the query. For performance reasons, it is recommended
        to not download the entire set of CFS 6 hourly data. 
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    1) The download URLs
    2) The list of filenames in the CFS Flux directory
    """
        
    final_date, init, files = forecast_file_times('flux',
                                            proxies,
                                            final_forecast_hour)
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound) 
        
    # This section handles the final forecast hour for the filename
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/18/6hrly_grib_01/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/12/6hrly_grib_01/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/06/6hrly_grib_01/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/00/6hrly_grib_01/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01/")
    
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)
        
    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file=flxf{final_date}.01.{init}18.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file=flxf{final_date}.01.{init}12.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file=flxf{final_date}.01.{init}06.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file=flxf{final_date}.01.{init}00.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file=flxf{final_date}.01.{init}18.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file=flxf{final_date}.01.{init}12.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file=flxf{final_date}.01.{init}06.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file=flxf{final_date}.01.{init}00.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"flxf{final_date}.01.{init}18.grb2"
    f_12z = f"flxf{final_date}.01.{init}12.grb2"
    f_06z = f"flxf{final_date}.01.{init}06.grb2"
    f_00z = f"flxf{final_date}.01.{init}00.grb2"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(60)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
                    y_00.close()
                    break
                except Exception as e:
                    i = i       
                    

    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(60)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_00.close()
                    break
                except Exception as e:
                    i = i         
 
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z,
        today_12z,
        today_06z,
        today_00z,
        yd_18z,
        yd_12z,
        yd_06z,
        yd_00z
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
    
    # Testing the status code and then returning the first link with a status code of 200

    for response, url in zip(responses, urls):
        if response.status_code == 200:
            url = url
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
        
    urls = []
    if responses[0].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file={file}&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                    f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                    f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                    f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code != 200 and responses[4].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code != 200 and responses[4].status_code != 200 and responses[5].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code != 200 and responses[4].status_code != 200 and responses[5].status_code != 200 and responses[6].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    else:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)

        
    
    return urls, files

def cfs_pressure_url_scanner(western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          variables,
                          final_forecast_hour):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) western_bound (Float or Integer) - The western bound of the data needed. 

    2) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    3) northern_bound (Float or Integer) - The northern bound of the data needed.

    4) southern_bound (Float or Integer) - The southern bound of the data needed.

   5) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                                
    6) variables (List) - A list of variable names the user wants to download in plain language. 
    
        Variable Name List for CFS Pressure
        -----------------------------------
            'best lifted index'
            '5 wave geopotential height anomaly'
            '5 wave geopotential height'
            'absolute vorticity'
            'convective precipitation'
            'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'convective inhibition'
            'cloud mixing ratio'
            'categorical rain'
            'categorical snow'
            'cloud water'
            'dew point'
            'geopotential height anomaly'
            'geopotential height'
            'storm relative helicity'
            'surface lifted index'
            'large scale non-convective precipitation'
            'ozone mixing ratio'
            'parcel lifted index (to 500mb)'
            'potential temperature'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'specific humidity'
            'stream function'
            'temperature'
            'total ozone'
            'u-component of wind'
            'u-component of storm motion'
            'v-component of wind'
            'velocity potential'
            'v-component of storm motion'
            'vertical velocity (pressure)'
            'vertical speed shear'
            
    7) final_forecast_hour (Integer) - The last forecast hour of the query. For performance reasons, it is recommended
        to not download the entire set of CFS 6 hourly data. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    1) The download URLs
    2) The list of filenames in the CFS Pressure directory
    """
        
    final_date, init, files = forecast_file_times('pressure',
                                            proxies,
                                            final_forecast_hour)
    
    # Converts the longitude from -180 to 180 into 0 to 360
    western_bound, eastern_bound = convert_lon(western_bound, eastern_bound) 
        
    # This section handles the final forecast hour for the filename
           
    # These are the different download URLs for the various runtimes in the past 24 hours
    
    # URLs to scan for the latest file
    today_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/18/6hrly_grib_01/")
    today_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/12/6hrly_grib_01/")
    today_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/06/6hrly_grib_01/")
    today_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{now.strftime('%Y%m%d')}/00/6hrly_grib_01/")
    
    yesterday_18z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/18/6hrly_grib_01/")
    yesterday_12z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/12/6hrly_grib_01/")
    yesterday_06z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/06/6hrly_grib_01/")
    yesterday_00z_scan = (f"https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs.{yd.strftime('%Y%m%d')}/00/6hrly_grib_01/")
    
    # Gets the variable list in a string format convered to GRIB filter keys
    
    keys = key_list(variables)
    params = result_string(keys)
        
    # Today's runs
    today_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}18.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}12.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}06.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}00.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}18.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}12.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}06.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file=pgbf{final_date}.01.{init}00.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"pgbf{final_date}.01.{init}18.grb2"
    f_12z = f"pgbf{final_date}.01.{init}12.grb2"
    f_06z = f"pgbf{final_date}.01.{init}06.grb2"
    f_00z = f"pgbf{final_date}.01.{init}00.grb2"
    
    # Tests the connection for each link. 
    # The first link with a response of 200 will be the download link
    
    # This is if the user has proxy servers disabled
    
    if proxies == None:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(60)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True)
                    y_00.close()
                    break
                except Exception as e:
                    i = i       
                    

    # This is if the user has a VPN/Proxy Server connection enabled
    else:
        try:
            t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
            t_18.close()
            t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
            t_12.close()
            t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
            t_06.close()
            t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
            t_00.close()
            y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
            y_18.close()
            y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
            y_12.close()
            y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
            y_06.close()
            y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
            y_00.close()
        except Exception as e:
            for i in range(0, 5, 1):
                time.sleep(60)
                try:
                    t_18 = requests.get(f"{today_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    t_18.close()
                    t_12 = requests.get(f"{today_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    t_12.close()
                    t_06 = requests.get(f"{today_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    t_06.close()
                    t_00 = requests.get(f"{today_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    t_00.close()
                    y_18 = requests.get(f"{yesterday_18z_scan}{f_18z}", stream=True, proxies=proxies)
                    y_18.close()
                    y_12 = requests.get(f"{yesterday_12z_scan}{f_12z}", stream=True, proxies=proxies)
                    y_12.close()
                    y_06 = requests.get(f"{yesterday_06z_scan}{f_06z}", stream=True, proxies=proxies)
                    y_06.close()
                    y_00 = requests.get(f"{yesterday_00z_scan}{f_00z}", stream=True, proxies=proxies)
                    y_00.close()
                    break
                except Exception as e:
                    i = i         
 
        
    # Creates a list of URLs and URL responses to loop through when checking
    
    urls = [
        today_18z,
        today_12z,
        today_06z,
        today_00z,
        yd_18z,
        yd_12z,
        yd_06z,
        yd_00z
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
    
    # Testing the status code and then returning the first link with a status code of 200

    for response, url in zip(responses, urls):
        if response.status_code == 200:
            url = url
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
        
    urls = []
    if responses[0].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file={file}&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                    f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                    f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                    f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code != 200 and responses[4].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code != 200 and responses[4].status_code != 200 and responses[5].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    elif responses[0].status_code != 200 and responses[1].status_code != 200 and responses[2].status_code != 200 and responses[3].status_code != 200 and responses[4].status_code != 200 and responses[5].status_code != 200 and responses[6].status_code == 200:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    else:
        for file in files:
            url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_pgb.pl"
                    f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file={file}&{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            urls.append(url)
    
    return urls, files