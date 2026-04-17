"""
This file hosts the functions that downloads the latest radar data and return a Py-ART object.


(C) Eric J. Drewitz 2025-2026
"""

import wxdata.client.client as _client
import os as _os
import warnings as _warnings
_warnings.filterwarnings('ignore')

from pathlib import Path as _Path
from wxdata.radar.url_scanner import scan_radar_directory as _scan_radar_directory
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

try:
    from datetime import(
        datetime as _datetime,
        UTC as _UTC
    )
except Exception as e:
    from datetime import datetime as _datetime 
    
try:
    _now = _datetime.now(_UTC)
except Exception as e:
    _now = _datetime.utcnow()
    
    
def download_current_single_station_nexrad2_radar_data(site_id,
                                                        hours=3,
                                                        path=f"Radar Data",
                                                        proxies=None,
                                                        clear_recycle_bin=False,
                                                        mode='precipitation',
                                                        notifications='off'):
    
    """
    This function downloads the latest NEXRAD2 Radar Data from NOAAs Open Data Amazon AWS Server and returns
    a list of Py-ART objects for a user-specified site ID and user-specified period of time.
    
    Required Arguments:
    
    1) site_id (String) - The 4-letter ID of the radar site.
    
    Optional Arguments:
    
    1) hours (Integer) - Default=3. The amount of hours to query (hours=3 --> current to current -3 hours).
    
    2) path (String) - Default="Radar Data". The parent directory of the radar data on the local computer.
    
    3) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port" ---> download_current_single_station_nexrad2_radar_data(bucket,
                                                                                                                            key,
                                                                                                                            path,
                                                                                                                            filenames,
                                                                                                                            proxies=proxies)
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    5) mode (String) - Default='precipitation'. When in 'precipitation' mode, data querying is based on 10 scans per hour.
        When in 'clear air' mode, data querying is based on 7 scans per hour.
        
    6) notifications (String) - Default='on'. When set to 'on' a print statement to the user will tell the user their file saved to the path
        they specified. 
        
    Returns
    -------
    
    A list of Py-ART Radar Objects for a user-specified station for a user-specified period of time.
    """
    
    site_id = site_id.upper()
    mode = mode.lower()
    notifications = notifications.lower()
    
    import pyart
    
    if proxies == None:
        pass
    else:
        _os.environ['http_proxy'] = proxies
        _os.environ['https_proxy'] = proxies
    
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
                                    _now, 
                                    hours,
                                    mode)
        
    if len(data) == 2:
        _client.get_open_aws_data("unidata-nexrad-level2",
                                    data[0],
                                    f"{path}/{site_id.upper()}",
                                    data[1],
                                    notifications=notifications)
    else:
        _client.get_open_aws_data("unidata-nexrad-level2",
                                    data[0],
                                    f"{path}/{site_id.upper()}",
                                    data[1],
                                    notifications=notifications)
                
        _client.get_open_aws_data("unidata-nexrad-level2",
                                    data[2],
                                    f"{path}/{site_id.upper()}",
                                    data[3],
                                    notifications=notifications,
                                    clear_data=False)
            
    files = []
    for file in _os.listdir(f"{path}/{site_id.upper()}"):
        files.append(file)
        
    files.reverse()
    radars = []
    for file in files:
        radar = pyart.io.read(_Path(f"{path}/{site_id.upper()}/{file}"))
        radars.append(radar)
        
    radars.reverse()
        
    return radars


def download_current_multi_station_nexrad2_radar_data(site_ids,
                                                        hours=3,
                                                        path=f"Radar Data",
                                                        proxies=None,
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
    
    3) proxies (String or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies="http://your-proxy-address:port" ---> download_current_single_station_nexrad2_radar_data(bucket,
                                                                                                                            key,
                                                                                                                            path,
                                                                                                                            filenames,
                                                                                                                            proxies=proxies)
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    5) mode (String) - Default='precipitation'. When in 'precipitation' mode, data querying is based on 10 scans per hour.
        When in 'clear air' mode, data querying is based on 7 scans per hour.
        
    6) notifications (String) - Default='on'. When set to 'on' a print statement to the user will tell the user their file saved to the path
        they specified. 
        
    Returns
    -------
    
    A list of Py-ART Radar Objects for a user-specified list of stations and for a user-specified period of time.
    The user-specified period of time is the same for both stations. 
    """
    
    radars = []
    for site_id in site_ids:
        radar = download_current_single_station_nexrad2_radar_data(site_id,
                                                        hours=hours,
                                                        path=path,
                                                        proxies=proxies,
                                                        clear_recycle_bin=clear_recycle_bin,
                                                        mode=mode,
                                                        notifications=notifications)
        radars.append(radar)
        
    return radars
    
    