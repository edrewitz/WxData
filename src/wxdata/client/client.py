"""
This file hosts the functions that are the client that retrieves the data from the data server and stores the data locally.

These functions are compatible with users on VPN/PROXY connections as well as normal connections.

1) get_gridded_data
2) get_csv_data
3) get_excel_data
5) get_open_aws_data
6) byte_range_request

(C) Eric J. Drewitz 2025-2026
"""

import itertools as _itertools
import requests as _requests
import time as _time
import sys as _sys
import os as _os
import pandas as _pd

import warnings as _warnings
_warnings.filterwarnings('ignore')

from io import BytesIO as _BytesIO
from datetime import(
    datetime as _datetime, 
    timedelta as _timedelta
)

from wxdata.utils.nomads_gribfilter import key_list as _key_list
from wxdata.client.level_coords import get_level_expression as _get_level_expression
from wxdata.utils.progress_bar import progress_bar as _progress_bar
from wxdata.client.byte_range import download_grib_data_by_byte_range as _download_grib_data_by_byte_range
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

# Getting yesterday's date for the default end date for the xmACIS2 client

_now = _datetime.now()
_yesterday = _now - _timedelta(days=1)

_year = _yesterday.year
_month = _yesterday.month
_day = _yesterday.day

if _month < 10:
    if _day >= 10:
        _yesterday = f"{_year}-0{_month}-{_day}"
    else:
        _yesterday = f"{_year}-0{_month}-0{_day}"   
else:
    if _day >= 10:
        _yesterday = f"{_year}-{_month}-{_day}"
    else:
        _yesterday = f"{_year}-{_month}-0{_day}" 

def get_gridded_data(url,
             path,
             filename,
             proxies=None,
             chunk_size=8192,
             notifications='on',
             clear_recycle_bin=False):
    
    """
    This function is the client that retrieves gridded weather/climate data (GRIB2 and NETCDF) files. 
    This client supports VPN/PROXY connections. 
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
    
    Returns
    -------
    
    Gridded weather/climate data files (GRIB2 or NETCDF) saved to {path}    
    """
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    try:
        _os.makedirs(f"{path}")
    except Exception as e:
        pass

    if proxies == None:
        try:
            with _requests.get(url, stream=True) as r:
                r.raise_for_status() 
                _progress_bar(r,
                                path,
                                filename,
                                blocksize=chunk_size)
            if notifications == 'on':
                print(f"Successfully saved {filename} to f:{path}")
            else:
                pass
        except _requests.exceptions.RequestException as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    with _requests.get(url, stream=True) as r:
                        r.raise_for_status() 
                        _progress_bar(r,
                                        path,
                                        filename,
                                        blocksize=chunk_size)
                    if notifications == 'on':
                        print(f"Successfully saved {filename} to f:{path}")  
                    break
                except _requests.exceptions.RequestException as e:
                    i = i 
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1)      
                        
        finally:
            if r:
                r.close() # Ensure the connection is closed.
            
    else:
        try:
            with _requests.get(url, stream=True, proxies=proxies) as r:
                r.raise_for_status() 
                _progress_bar(r,
                                path,
                                filename,
                                blocksize=chunk_size)
            if notifications == 'on':
                print(f"Successfully saved {filename} to f:{path}")
            else:
                pass
        except _requests.exceptions.RequestException as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    with _requests.get(url, stream=True, proxies=proxies) as r:
                        r.raise_for_status() 
                        _progress_bar(r,
                                        path,
                                        filename,
                                        blocksize=chunk_size)
                    if notifications == 'on':
                        print(f"Successfully saved {filename} to f:{path}")  
                    break
                except _requests.exceptions.RequestException as e:
                    i = i 
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1)    
                        
        finally:
            if r:
                r.close() # Ensure the connection is closed.
                        
                        
def get_csv_data(url,
                 path,
                 filename,
                 proxies=None,
                 notifications='on',
                 return_pandas_df=True,
                 clear_recycle_bin=False):
    
    """
    This function is the client that retrieves CSV files from the web.
    This client supports VPN/PROXY connections. 
    User also has the ability to read the CSV file and return a Pandas.DataFrame()
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    2) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    3) return_pandas_df (Boolean) - Default=True. When set to True, a Pandas.DataFrame() of the data inside the CSV file will be returned to the user. 
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
    
    
    Returns
    -------
    
    A CSV file saved to {path}
    
    if return_pandas_df=True - A Pandas.DataFrame()
    """
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    try:
        _os.makedirs(f"{path}")
    except Exception as e:
        pass
    
    if proxies==None:
        try:
            response = _requests.get(url)
        except Exception as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    response = _requests.get(url)
                    break
                except Exception as e:
                    i = i                    
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1)    
        finally:
            if response:
                response.close() # Ensure the connection is closed.
                        
    else:
        try:
            response = _requests.get(url, proxies=proxies)
        except Exception as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    response = _requests.get(url, proxies=proxies)
                    break
                except Exception as e:
                    i = i                    
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1) 

                
                 

    data_stream = _BytesIO(response.content)
    if response:
        response.close() # Ensure the connection is closed.
    
    df = _pd.read_csv(data_stream)
    
    df.to_csv(f"{path}/{filename}", index=False)
    if notifications == True:
        print(f"{filename} saved to {path}")
    else:
        pass
    
    if return_pandas_df == True:
        
        return df
    
    else:
        pass
    
def get_excel_data(url,
                 path,
                 filename,
                 sheet_name,
                 proxies=None,
                 notifications='on',
                 return_pandas_df=True,
                 clear_recycle_bin=False):
    
    """
    This function is the client that retrieves Excel files from the web.
    This client supports VPN/PROXY connections. 
    User also has the ability to read the Excel file and return a Pandas.DataFrame()
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    4) sheet_name (String) - The name of the sheet in the excel file to be converted into a pandas.DataFrame. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    2) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    3) return_pandas_df (Boolean) - Default=True. When set to True, a Pandas.DataFrame() of the data inside the CSV file will be returned to the user. 
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
    
    
    Returns
    -------
    
    An Excel file saved to {path}
    
    if return_pandas_df=True - A Pandas.DataFrame()
    """
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    try:
        _os.makedirs(f"{path}")
    except Exception as e:
        pass
    
    if proxies==None:
        try:
            response = _requests.get(url)
        except Exception as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    response = _requests.get(url)
                    break
                except Exception as e:
                    i = i                    
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1)    
        finally:
            if response:
                response.close() # Ensure the connection is closed.
                        
    else:
        try:
            response = _requests.get(url, proxies=proxies)
        except Exception as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    response = _requests.get(url, proxies=proxies)
                    break
                except Exception as e:
                    i = i                    
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1) 

                
                 

    data_stream = _BytesIO(response.content)
    if response:
        response.close() # Ensure the connection is closed.
    
    df = _pd.read_excel(data_stream)
    
    df.to_excel(f"{path}/{filename}", index=False)
    
    if notifications == True:
        print(f"{filename} saved to {path}")
    else:
        pass
    
    if return_pandas_df == True:
        
        df = _pd.read_excel(f"{path}/{filename}", sheet_name=sheet_name)
        
        return df
    
    else:
        pass
    
    
def get_aws_open_data(url,
                    path,
                    filename,
                    proxies=None,
                    chunk_size=8192,
                    notifications='on',
                    clear_recycle_bin=False):
    
    """
    This function is the client that retrieves Open Data from Amazon AWS Servers. 
    This client supports VPN/PROXY connections. 
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
    
    Returns
    -------
    
    Files from AWS Open Data.  
    """
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    try:
        _os.makedirs(f"{path}")
    except Exception as e:
        pass

    if proxies == None:
        
        try:
            with _requests.get(f"{url}{filename}", stream=True, allow_redirects=True, timeout=60) as r:
                r.raise_for_status() 
                _progress_bar(r,
                                path,
                                filename,
                                blocksize=chunk_size)
            if notifications == 'on':
                print(f"Successfully saved {filename} to f:{path}")
            else:
                pass
        except _requests.exceptions.RequestException as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    with _requests.get(f"{url}{filename}", stream=True, allow_redirects=True, timeout=60) as r:
                        r.raise_for_status() 
                        _progress_bar(r,
                                        path,
                                        filename,
                                        blocksize=chunk_size)
                    if notifications == 'on':
                        print(f"Successfully saved {filename} to f:{path}")  
                    break
                except _requests.exceptions.RequestException as e:
                    i = i 
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1)      
                        
        finally:
            if r:
                r.close() # Ensure the connection is closed.
            
    else:
        try:
            with _requests.get(f"{url}{filename}", stream=True, proxies=proxies, allow_redirects=True, timeout=60) as r:
                r.raise_for_status() 
                _progress_bar(r,
                                path,
                                filename,
                                blocksize=chunk_size)
            if notifications == 'on':
                print(f"Successfully saved {filename} to f:{path}")
            else:
                pass
        except _requests.exceptions.RequestException as e:
            for i in range(0, 10, 1):
                if i < 3:
                    print(f"Alert: Network connection unstable.\nWaiting 30 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(30)
                else:
                    print(f"Alert: Network connection unstable.\nWaiting 60 seconds then automatically trying again.\nAttempts remaining: {10 - i}")
                    _time.sleep(60)  
                    
                try:
                    with _requests.get(f"{url}{filename}", stream=True, proxies=proxies, allow_redirects=True, timeout=60) as r:
                        r.raise_for_status() 
                        _progress_bar(r,
                                        path,
                                        filename,
                                        blocksize=chunk_size)
                    if notifications == 'on':
                        print(f"Successfully saved {filename} to f:{path}")  
                    break
                except _requests.exceptions.RequestException as e:
                    i = i 
                    if i >= 9:
                        print(f"Error - File Cannot Be Downloaded.\nError Code: {e}")    
                        _sys.exit(1)    
                        
        finally:
            if r:
                r.close() # Ensure the connection is closed.
                
                
def byte_range_request(grib_url,
                      idx_url,
                      variables,
                      levels,
                      level_type,
                      path,
                      filename,
                      proxies=None,
                      chunk_size=1024,
                      notifications='on',
                      clear_recycle_bin=False):
    
    """
    This client downloads GRIB data for a specific variable that is defined by the range in bytes in that GRIB file. 
    This is useful when the user wants to download a GRIB file where there is no GRIB filter present, especially when the file size is large.
    This will allow users to download the variable they are interested in and filter out all other variables prior to downloading.
    
    Required Arguments:
    
    1) grib_url (String) - The URL of the GRIB file that will be downloaded.
    
    2) idx_url (String) - The URL of the index file that corresponds to the GRIB file (ends in .idx).
    
    3) variables (String List) - The list of variables to be downloaded.
    
    4) levels (Float or Integer List) - The list of pressure or height levels. 
    
    5) level_type (String) - The type of level.
    
        Level Types
        -----------
        
        'hybrid'
        'entire atmosphere'
        'surface':'surface',
        'boundary layer'
        'pressure'
        'mean sea level'
        'height above ground'
        'height below ground'
        'height above sea level'
        'entire atmosphere single layer'
        'low cloud layer'
        'middle cloud layer'
        'high cloud layer'
        'cloud ceiling'
        'tropopause'
        'max wind'
        'isothermal'
        'highest tropospheric freezing level'
        'sigma layer'
        'sigma level'
        'potential vorticity surface'
        'reserved'
    
    6) path (String) - The directory where the file is saved to. 
    
    7) filename (String) - The name the user wishes to save the file as. 
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='on'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - Default=False. When set to True, the contents in your recycle/trash bin 
    will be deleted with each run of the program you are calling WxData. This setting is to help preserve memory on the machine. 
        
    Returns
    -------
    
    Downloads a partial GRIB file consisting of the variable the user specifies.     
    """
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass
    
    try:
        _os.makedirs(f"{path}")
    except Exception as e:
        pass

    variables = _key_list(variables)
    
    try:

        if proxies == None:
            try:
                idx_text = _requests.get(idx_url).text
            except Exception as e:
                for i in range(0, 10, 1):
                    print(f"Client lost connection to server - Waiting 30 seconds and trying again.")
                    _time.sleep(30)
                    try:
                        idx_text = _requests.get(idx_url).text
                        break
                    except Exception as e:
                        i = i
                        if i >= 9:
                            print(f"Client cannot establish connection to server - System Exit.")
                            _sys.exit(1)
                        
        else:
            try:
                idx_text = _requests.get(idx_url, proxies=proxies).text
            except Exception as e:
                for i in range(0, 10, 1):
                    print(f"Client lost connection to server - Waiting 30 seconds and trying again.")
                    _time.sleep(30)
                    try:
                        idx_text = _requests.get(idx_url, proxies=proxies).text
                        break
                    except Exception as e:
                        i = i
                        if i >= 9:
                            print(f"Client cannot establish connection to server - System Exit.")
                            _sys.exit(1)
            
        records = []
        for line in idx_text.strip().splitlines():
            parts = line.split(':')
            try:
                msg_no = int(parts[0])
            except Exception as e:
                msg_no = float(parts[0])
            try:
                offset = int(parts[1])
            except Exception as e:
                offset = float(parts[1])
            var = parts[3]
            lev = parts[4]
            records.append({
                "msg": msg_no,
                "offset": offset,
                "var": var,
                "lev": lev
            })
            
        req_levels, levels = _get_level_expression(levels,
                                                    level_type)
        
        if levels is not None:
            reqs = list(_itertools.product(variables, req_levels))
        else:
            reqs = []
            for v in variables:
                req = (v, req_levels)
                reqs.append(req)

        ranges = {}
        for v, l in reqs:
            matches = [r for r in records if r["var"] == v and r["lev"] == l]
            if not matches:
                print(f"{v} is not a valid variable OR {l} is not a valid level.")
                print(f"Please visit {idx_url} to look at the variables in the GRIB file meta-data")
                _sys.exit(1)
            else:
                pass

            rec = matches[0]
            start = rec["offset"]

            idx = records.index(rec)
            if idx < len(records) - 1:
                end = records[idx + 1]["offset"] - 1
            else:
                end = None

            ranges[(v, l)] = (start, end)
        
        _download_grib_data_by_byte_range(ranges,
                                chunk_size,
                                path,
                                filename,
                                grib_url,
                                start,
                                end,
                                proxies)
        
        if notifications == 'on':
            print(f"{filename} saved to {path}")
            
    except Exception as e:
        for i in range(0, 10, 1):
            _time.sleep(30)
            try:
                
                if proxies == None:
                    try:
                        idx_text = _requests.get(idx_url).text
                    except Exception as e:
                        for i in range(0, 10, 1):
                            print(f"Client lost connection to server - Waiting 30 seconds and trying again.")
                            _time.sleep(30)
                            try:
                                idx_text = _requests.get(idx_url).text
                                break
                            except Exception as e:
                                i = i
                                if i >= 9:
                                    print(f"Client cannot establish connection to server - System Exit.")
                                    _sys.exit(1)
                                
                else:
                    try:
                        idx_text = _requests.get(idx_url, proxies=proxies).text
                    except Exception as e:
                        for i in range(0, 10, 1):
                            print(f"Client lost connection to server - Waiting 30 seconds and trying again.")
                            _time.sleep(30)
                            try:
                                idx_text = _requests.get(idx_url, proxies=proxies).text
                                break
                            except Exception as e:
                                i = i
                                if i >= 9:
                                    print(f"Client cannot establish connection to server - System Exit.")
                                    _sys.exit(1)
                    
                records = []
                for line in idx_text.strip().splitlines():
                    parts = line.split(':')
                    try:
                        msg_no = int(parts[0])
                    except Exception as e:
                        msg_no = float(parts[0])
                    try:
                        offset = int(parts[1])
                    except Exception as e:
                        offset = float(parts[1])
                    var = parts[3]
                    lev = parts[4]
                    records.append({
                        "msg": msg_no,
                        "offset": offset,
                        "var": var,
                        "lev": lev
                    })
                    
                req_levels, levels = _get_level_expression(levels,
                                                            level_type)
                
                if levels is not None:
                    reqs = list(_itertools.product(variables, req_levels))
                else:
                    reqs = []
                    for v in variables:
                        req = (v, req_levels)
                        reqs.append(req)

                ranges = {}
                for v, l in reqs:
                    matches = [r for r in records if r["var"] == v and r["lev"] == l]
                    if not matches:
                        print(f"{v} is not a valid variable OR {l} is not a valid level.")
                        print(f"Please visit {idx_url} to look at the variables in the GRIB file meta-data")
                        _sys.exit(1)
                    else:
                        pass

                    rec = matches[0]
                    start = rec["offset"]

                    idx = records.index(rec)
                    if idx < len(records) - 1:
                        end = records[idx + 1]["offset"] - 1
                    else:
                        end = None

                    ranges[(v, l)] = (start, end)
                
                _download_grib_data_by_byte_range(ranges,
                                        chunk_size,
                                        path,
                                        filename,
                                        grib_url,
                                        start,
                                        end,
                                        proxies)
                
                if notifications == 'on':
                    print(f"{filename} saved to {path}")
                    
                break
            except Exception as e:
                i = i
        
    
        