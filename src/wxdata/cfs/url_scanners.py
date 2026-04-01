"""
This file hosts the CFS URL Scanner Functions.

These functions return the URL and filename for the latest available data on the dataservers.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import os

from urllib.parse import urlparse, parse_qs
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
                        proxies):
    
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
    
    Returns
    -------
    
    The datetimes of the final forecast file and model initialization in string format.    
    """
    
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
            response = requests.get(url, stream=True)
        else:
            response = requests.get(url, stream=True, proxies=proxies)
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
        key = f"flxf"    
        for f in fnames:
            if key in f:
                files.append(f)
                
    file = files[-1]
    date = file[4:14]
    init = file[18:26]
    
    return date, init

def cfs_flux_url_scanner(final_forecast_datetime, 
                          western_bound, 
                          eastern_bound, 
                          northern_bound, 
                          southern_bound, 
                          proxies, 
                          step, 
                          variables):
    
    
    """
    This function scans for the latest model run and returns the runtime and the download URL
    
    Required Arguments:
    
    1) final_forecast_datetime (String) - The date and time for the final forecast hour in UTC.
        Format: 'YYYY-mm-dd-HH'
    
    2) western_bound (Float or Integer) - The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - The northern bound of the data needed.

    5) southern_bound (Float or Integer) - The southern bound of the data needed.

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    7) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 
    
    8) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    9) variables (List) - A list of variable names the user wants to download in plain language. 
    
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
    
    The model runtime and the download URL.     
    """
    
    date = f"{final_forecast_datetime[0:3]}{final_forecast_datetime[5:6]}{final_forecast_datetime[8:9]}{final_forecast_datetime[11:12]}"
    
    final_date, init = forecast_file_times('flux',
                                            proxies)
    
    dt1 = datetime.strptime(date, "%Y%m%d%H")
    dt2 = datetime.strptime(final_date, "%Y%m%d%H")
    dt3 = datetime.strptime(init, "%Y%m%d")
    
    if dt1 > dt2:
        print(f"User entered a date beyond the forecast period.")
        print(f"Defaulting to the final forecast date/time of {dt2.strftime('%m/%d/%Y %H:00 UTC')}")
        dt1 = dt2
    else:
        dt1 = dt1
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
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}18.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}12.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}06.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    today_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{now.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}00.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    # Yesterday's runs
    yd_18z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F18%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}18.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_12z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F12%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}12.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_06z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F06%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}06.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
    
    yd_00z = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_cfs_flx.pl"
                 f"?dir=%2Fcfs.{yd.strftime('%Y%m%d')}%2F00%2F6hrly_grib_01&file=flxf{dt1}.01.{dt3}00.grb2&{params}&"
                 f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")    
    

    # The filenames for the different run times
    f_18z = f"flxf{dt1}.01.{dt3}18.grb2"
    f_12z = f"flxf{dt1}.01.{dt3}12.grb2"
    f_06z = f"flxf{dt1}.01.{dt3}06.grb2"
    f_00z = f"flxf{dt1}.01.{dt3}00.grb2"
    
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
            run = int(f"{url[78]}{url[79]}")
            break        
    
    try:
        url = url
    except Exception as e:
        print(f"Latest forecast data is over 24 hours old. Aborting.....")
        sys.exit(1)
    
    if step == 6:
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
    elif step == 3:
        if int(final_forecast_hour) > 100:
            step = 3
            stop = 99 + step
            start = 102
        else:
            step = 3
            stop = int(final_forecast_hour) + step
    else:
        print("ERROR! User entered an invalid step value\nDefaulting to 6 hourly.")
        if int(final_forecast_hour) > 100:
            step = 6
            stop = 96 + step
            start = 102
        else:
            step = 6
            stop = int(final_forecast_hour) + step
        
        
    urls = []
    
    
    if url == today_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == today_00z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{now.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_18z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F18%2Fatmos&file=gfs.t18z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_12z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F12%2Fatmos&file=gfs.t12z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    elif url == yd_06z:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F06%2Fatmos&file=gfs.t06z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
                    
    else:
        for i in range(0, stop, step):
            if i < 10:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f00{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
            else:
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                    f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f0{i}{params}&"
                    f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
            urls.append(url)
                
        if int(final_forecast_hour) > 100:
            for i in range(start, int(final_forecast_hour) + step, step):
                url = (f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl"
                        f"?dir=%2Fgfs.{yd.strftime('%Y%m%d')}%2F00%2Fatmos&file=gfs.t00z.pgrb2full.0p50.f{i}{params}&"
                        f"all_lev=on&subregion=&toplat={northern_bound}&leftlon={western_bound}&rightlon={eastern_bound}&bottomlat={southern_bound}")
                
                urls.append(url)
        

        
    # Extract the filename
    # Parse the URL
    filenames = []
    for url in urls:
        
        parsed_url = urlparse(url)

        # Extract the query string
        query_string = parsed_url.query

        # Parse the query string into a dictionary of parameters
        query_params = parse_qs(query_string)

        # Access individual parameters
        filename = query_params.get('file', [''])[0] 
        
        filenames.append(filename)
        
    
    return urls, filenames, run