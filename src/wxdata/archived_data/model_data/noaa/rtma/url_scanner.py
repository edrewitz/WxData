"""
This file scans the Amazon Web Services (AWS) Archive for the Real Time Mesoscale Analysis for a specific region and specific date.

(C) Eric J. Drewitz 2025-2026
"""

import requests
import sys

from datetime import datetime

start = datetime.strptime("2020010100", "%Y%m%d%H")

PREFIX = f"https://noaa-rtma-pds.s3.amazonaws.com/"


def rtma_url_scanner(date,
                     run,
                     model, 
                    cat,
                    proxies):
    
    """
    This function scans for the requested RTMA data for a specific region at a specific time. 
    
    Required Arguments:
    
    1) date (String) - The date of the RTMA data. Format: "YYYY-mm-dd"
    
    2) run (Integer or String) - The runtime for the RTMA. This can be entered as an integer from 0 to 24 or a string
        from '00' to '24'. 
    
    3) model (String) - The RTMA Model:
    
    RTMA Models:
    i) RTMA - CONUS
    ii) AK RTMA - Alaska
    iii) HI RTMA - Hawaii
    iv) GU RTMA - Guam
    v) PR RTMA - Puerto Rico
    
    4) cat (String) - The category of the variables. 
    
    i) Analysis
    ii) Error
    iii) Forecast
    
    5) proxies (dict or None) - If the user is using a proxy server, the user must change the following:

    proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
    
    Returns
    -------
    
    The URL path to the file and the filename for the most recent RTMA Dataset.
    
    """
    
    if type(date) != type(start):
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = datetime.strptime(date, "%Y%m%d")
    else:
        date = date
        
    if type(run) == type(1):
        if run <10:
            run = f"0{run}"
        else:
            run = f"{run}"
    else:
        run = run
    
    model = model.upper()
    cat = cat.upper()
        
    if model == 'RTMA':
        directory = 'rtma2p5'
    elif model == 'AK RTMA':
        directory = 'akrtma'
    elif model == 'HI RTMA':
        directory = 'hirtma'
    elif model == 'GU RTMA':
        directory = 'gurtma'
    else:
        directory = 'prrtma'
          
    if cat == 'ANALYSIS':
        f_cat = 'anl'
    elif cat == 'ERROR':
        f_cat = 'err'
    else:
        f_cat = 'ges'
            
    
    url = f"{PREFIX}{directory}.{date.strftime('%Y%m%d')}/"    

    
    
    if model == 'AK RTMA':
        file = f"{directory}.t{run}z.2dvar{f_cat}_ndfd_3p0.grb2"
    
    elif model == 'RTMA':
        file = f"{directory}.t{run}z.2dvar{f_cat}_ndfd.grb2_wexp"
        
    else:
        file = f"{directory}.t{run}z.2dvar{f_cat}_ndfd.grb2"
    
    
    print(f"{url}{file}")
    try:
        if proxies == None:
            response = requests.get(f"{url}{file}",
                                    stream=True)
        else:
            response = requests.get(f"{url}{file}", 
                              stream=True, 
                              proxies=proxies)
    except Exception as e:
        print(f"{date.strftime('%Y%m%d %H')}z is not valid.")
        print(f"Double check your date. The record begins at: {start.strftime('%Y%m%d %H')}z")
        sys.exit(1)
        

    if response.status_code == 200:
        url = url
        file = file
    else:
        print(f"{date.strftime('%Y%m%d %H')}z is not valid.")
        print(f"Double check your date. The record begins at: {start.strftime('%Y%m%d %H')}z")
        sys.exit(1)

    return url, file

