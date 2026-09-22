"""
This file hosts the GEFS URL Scanner Functions.

These functions return the URLs for the Archived GEFS Data (hosted on Amazon Web Services & Google Cloud)

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys
import time

from wxdata.model_data.noaa.gefs.exception_messages import(    
    gefs0p50,
    gefs0p25
)

from datetime import datetime


# The earliest GEFS data hosted between AWS and Google Cloud is from 1/1/2017
start = datetime.strptime("2017010100", "%Y%m%d%H")

AWS = f"https://noaa-gefs-pds.s3.amazonaws.com"
GOOGLE = f"https://storage.googleapis.com/gfs-ensemble-forecast-system"

def gefs_0p50_url_scanner(date,
                          run,
                          cat, 
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

    3) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                            
    4) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.     
    """
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    source = source.lower()
            
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


    if source == 'aws':
        url = f"{AWS}/gefs.{date.strftime('%Y%m%d')}/{run}/atmos/pgrb2ap5/"
    else:
        url = f"{GOOGLE}/gefs.{date.strftime('%Y%m%d')}/{run}/atmos/pgrb2ap5/"
        
    file = f"ge{aa}.t{run}z.pgrb2a.0p50.f{final_forecast_hour}"
    
    if proxies == None:
        try:
            response = requests.get(f"{url}{file}", 
                                stream=True)
            response.close()
        except Exception as e:
            print(f"Error: Client unable to connect to {source.upper()} Server.")
            if source == 'aws':
                print(f"Rotating to Google Cloud.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'google')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
            else:
                print(f"Rotating to AWS.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'aws')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
                    
    else:
        try:
            response = requests.get(f"{url}{file}", 
                                stream=True,
                                proxies=proxies)
            response.close()
        except Exception as e:
            print(f"Error: Client unable to connect to {source.upper()} Server.")
            if source == 'aws':
                print(f"Rotating to Google Cloud.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'google')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
            else:
                print(f"Rotating to AWS.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'aws')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
                    
    if response.status_code == 200:
        url = url
    else:
        print(f"Error: Client unable to connect to {source.upper()} Server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                url = gefs_0p50_url_scanner(date,
                        run,
                        cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        'google')
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                sys.exit(1)
        else:
            print(f"Rotating to AWS.")
            try:
                url = gefs_0p50_url_scanner(date,
                        run,
                        cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        'aws')
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                sys.exit(1)
                    
    
    return url, date


def gefs_0p50_secondary_parameters_url_scanner(date,
                          run,
                          cat, 
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

    3) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                            
    4) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.     
    """
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    source = source.lower()
            
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


    if source == 'aws':
        url = f"{AWS}/gefs.{date.strftime('%Y%m%d')}/{run}/atmos/pgrb2bp5/"
    else:
        url = f"{GOOGLE}/gefs.{date.strftime('%Y%m%d')}/{run}/atmos/pgrb2bp5/"
        
    file = f"ge{aa}.t{run}z.pgrb2b.0p50.f{final_forecast_hour}"
    
    if proxies == None:
        try:
            response = requests.get(f"{url}{file}", 
                                stream=True)
            response.close()
        except Exception as e:
            print(f"Error: Client unable to connect to {source.upper()} Server.")
            if source == 'aws':
                print(f"Rotating to Google Cloud.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'google')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
            else:
                print(f"Rotating to AWS.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'aws')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
                    
    else:
        try:
            response = requests.get(f"{url}{file}", 
                                stream=True,
                                proxies=proxies)
            response.close()
        except Exception as e:
            print(f"Error: Client unable to connect to {source.upper()} Server.")
            if source == 'aws':
                print(f"Rotating to Google Cloud.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'google')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
            else:
                print(f"Rotating to AWS.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'aws')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
                    
    if response.status_code == 200:
        url = url
    else:
        print(f"Error: Client unable to connect to {source.upper()} Server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                url = gefs_0p50_url_scanner(date,
                        run,
                        cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        'google')
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                sys.exit(1)
        else:
            print(f"Rotating to AWS.")
            try:
                url = gefs_0p50_url_scanner(date,
                        run,
                        cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        'aws')
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                sys.exit(1)
                    
    
    return url, date
            

def gefs_0p25_url_scanner(date,
                          run,
                          cat, 
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

    3) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                            
    4) members (List) The individual ensemble members. There are 30 members in this ensemble.  
    
    5) source (String) - Default='noaa'. The data server the user wants to connect the client to.
    
        Server List
        -----------
        
        1) NOAA/NCEP/NOMADS - source='noaa'
        2) Amazon AWS - source='aws'
        3) Google Cloud - source='google'
    
    Optional Arguments: None
    
    
    Returns
    -------
    
    The model runtime, download URL and server response code.     
    """
    if type(date) == type(start):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    
    # Makes the category all lower case for consistency
    cat = cat.lower()
    
    source = source.lower()
            
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


    if source == 'aws':
        url = f"{AWS}/gefs.{date.strftime('%Y%m%d')}/{run}/atmos/pgrb2sp25/"
    else:
        url = f"{GOOGLE}/gefs.{date.strftime('%Y%m%d')}/{run}/atmos/pgrb2sp25/"
        
    file = f"ge{aa}.t{run}z.pgrb2s.0p25.f{final_forecast_hour}"
    
    if proxies == None:
        try:
            response = requests.get(f"{url}{file}", 
                                stream=True)
            response.close()
        except Exception as e:
            print(f"Error: Client unable to connect to {source.upper()} Server.")
            if source == 'aws':
                print(f"Rotating to Google Cloud.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'google')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
            else:
                print(f"Rotating to AWS.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'aws')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
                    
    else:
        try:
            response = requests.get(f"{url}{file}", 
                                stream=True,
                                proxies=proxies)
            response.close()
        except Exception as e:
            print(f"Error: Client unable to connect to {source.upper()} Server.")
            if source == 'aws':
                print(f"Rotating to Google Cloud.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'google')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
            else:
                print(f"Rotating to AWS.")
                try:
                    url = gefs_0p50_url_scanner(date,
                            run,
                            cat, 
                            final_forecast_hour, 
                            proxies, 
                            members,
                            'aws')
                except Exception as e:
                    print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                    sys.exit(1)
                    
    if response.status_code == 200:
        url = url
    else:
        print(f"Error: Client unable to connect to {source.upper()} Server.")
        if source == 'aws':
            print(f"Rotating to Google Cloud.")
            try:
                url = gefs_0p50_url_scanner(date,
                        run,
                        cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        'google')
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                sys.exit(1)
        else:
            print(f"Rotating to AWS.")
            try:
                url = gefs_0p50_url_scanner(date,
                        run,
                        cat, 
                        final_forecast_hour, 
                        proxies, 
                        members,
                        'aws')
            except Exception as e:
                print(f"Error: Client is unable to establish a connection to either server. - System Exit.")
                sys.exit(1)
                    
    
    return url, date