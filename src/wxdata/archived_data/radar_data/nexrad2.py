"""
This file hosts the functions that downloads the archived radar data and return a Py-ART object for the requested time.

This archive is hosted by Amazon Web Services (AWS)

(C) Eric J. Drewitz 2025-2026
"""

import wxdata.client.client as _client
import os as _os
import warnings as _warnings
_warnings.filterwarnings('ignore')

from pathlib import Path as _Path
from wxdata.observational_data.radar.url_scanner import scan_radar_directory as _scan_radar_directory
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)
    
from datetime import datetime as _datetime

_now = _datetime.now()
    
def download_archived_single_station_nexrad2_radar_data(site_id,
                                                        start_time,
                                                        hours=3,
                                                        path=f"Radar Data/Archive",
                                                        proxies=None,
                                                        chunk_size=8192,
                                                        clear_recycle_bin=False,
                                                        mode='precipitation',
                                                        notifications='off'):
    
    """
    This function downloads the latest NEXRAD2 Radar Data from NOAAs Open Data Amazon AWS Server and returns
    a list of Py-ART objects for a user-specified site ID and user-specified period of time.
    
    Required Arguments:
    
    1) site_id (String) - The 4-letter ID of the radar site.
    
    2) start_time (String or datetime object) - The time in 'YYYY-mm-dd:HH' of the last scan in the set.
        
        Example: start_time='2025-08-01:18' & hours = 3 = Radar scans from 2025-08-01:15 - 2025-08-01:18. 
    
    Optional Arguments:
    
    1) hours (Integer) - Default=3. The amount of hours to query (hours=3 --> start_time to start_time -3 hours).
    
    2) path (String) - Default="Radar Data". The parent directory of the radar data on the local computer.
    
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    4) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine.
        
    6) mode (String) - Default='precipitation'. When in 'precipitation' mode, data querying is based on 10 scans per hour.
        When in 'clear air' mode, data querying is based on 7 scans per hour.
        
    7) notifications (String) - Default='on'. When set to 'on' a print statement to the user will tell the user their file saved to the path
        they specified. 
        
    Returns
    -------
    
    A list of Py-ART Radar Objects for a user-specified station for a user-specified period of time.
    """
    
    site_id = site_id.upper()
    mode = mode.lower()
    notifications = notifications.lower()
    
    if type(start_time) == type(_now):
        pass
    else:
        start_time = _datetime.strptime(start_time, "%Y-%m-%d:%H")
    
    import pyart
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    try:
        _os.makedirs(f"{path}/{site_id.upper()}")
    except Exception as e:
        pass
    
    try:
        for file in _os.listdir(f"{path}/{site_id.upper()}"):
            _os.remove(f"{path}/{site_id.upper()}/{file}")
    except Exception as e:
        pass
    
    data = _scan_radar_directory(site_id,
                                    start_time, 
                                    hours,
                                    mode,
                                    proxies)
    
        
    if len(data) == 2:
        for filename in data[1]:
            _client.get_aws_open_data(data[0],
                                        f"{path}/{site_id.upper()}/{start_time.strftime('%Y%m%d%H')}",
                                        filename,
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)
    else:
        for filename in data[1]:
            _client.get_aws_open_data(data[0],
                                        f"{path}/{site_id.upper()}/{start_time.strftime('%Y%m%d%H')}",
                                        filename,
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=clear_recycle_bin)
            
        for filename in data[3]:
            _client.get_aws_open_data(data[2],
                                        f"{path}/{site_id.upper()}/{start_time.strftime('%Y%m%d%H')}",
                                        filename,
                                        proxies=proxies,
                                        chunk_size=chunk_size,
                                        notifications=notifications,
                                        clear_recycle_bin=False)
            
    files = []
    for file in _os.listdir(f"{path}/{site_id.upper()}/{start_time.strftime('%Y%m%d%H')}"):
        files.append(file)
        
    files.reverse()
    radars = []
    for file in files:
        radar = pyart.io.read(_Path(f"{path}/{site_id.upper()}/{start_time.strftime('%Y%m%d%H')}/{file}"))
        radars.append(radar)
        
    radars.reverse()
        
    return radars


def download_archived_multi_station_nexrad2_radar_data(site_ids,
                                                      start_time,
                                                        hours=3,
                                                        path=f"Radar Data/Archive",
                                                        proxies=None,
                                                        chunk_size=8192,
                                                        clear_recycle_bin=False,
                                                        mode='precipitation',
                                                        notifications='off'):
    
    """
    This function downloads the latest NEXRAD2 Radar Data from NOAAs Open Data Amazon AWS Server and returns
    a list of Py-ART objects for a user-specified list of site IDs and user-specified period of time.
    
    Required Arguments:
    
    1) site_ids (String List) - A list of the 4-letter IDs of the radar sites.
    
    Optional Arguments:
    
    1) hours (Integer) - Default=3. The amount of hours to query (hours=3 --> current to current -3 hours).
    
    2) path (String) - Default="Radar Data". The parent directory of the radar data on the local computer.
    
    3) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    4) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    5) clear_recycle_bin (Boolean) - Default=False. When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    6) mode (String) - Default='precipitation'. When in 'precipitation' mode, data querying is based on 10 scans per hour.
        When in 'clear air' mode, data querying is based on 7 scans per hour.
        
    7) notifications (String) - Default='on'. When set to 'on' a print statement to the user will tell the user their file saved to the path
        they specified. 
        
    Returns
    -------
    
    A list of Py-ART Radar Objects for a user-specified list of stations and for a user-specified period of time.
    The user-specified period of time is the same for both stations. 
    """
    
    radars = []
    for site_id in site_ids:
        radar = download_archived_single_station_nexrad2_radar_data(site_id,
                                                        start_time,
                                                        hours=hours,
                                                        path=path,
                                                        proxies=proxies,
                                                        chunk_size=chunk_size,
                                                        clear_recycle_bin=clear_recycle_bin,
                                                        mode=mode,
                                                        notifications=notifications)
        radars.append(radar)
        
    return radars
    
    