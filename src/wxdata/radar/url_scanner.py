"""
This file hosts the functions required to scan the radar directory for the needed files.

(C) Eric J. Drewitz 2025-2026
"""
import requests
import time
import xml.etree.ElementTree as ET
import warnings as warnings
warnings.filterwarnings('ignore')

from datetime import timedelta

def scan_radar_directory(site_id,
                         end, 
                         hours,
                         mode,
                         proxies):
    
    """
    This function returns the queried files for a given site_id (radar site) for a given time period defined as start to end. 
    
    Required Arguments:
    
    1) site_id (String) - The 4-Letter ID of the radar site.
    
    2) end (datetime) - The datetime object of the end time of the query.
    
    3) hours (Integer) - The amount of hours back to query.
                               
    4) mode (String) - When set to 'precipitation' there are about 10 files (scans) per hour.
        When set to 'clean air' there are about 7 files (scans) per hour. 
        
    5) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                               
    Optional Arguments: None
    
    Returns
    -------
    
    A list of all the data needed to make the request using the boto3 client. 
    """
    mode = mode.lower()
    start = end - timedelta(hours=hours)
    bucket = "https://unidata-nexrad-level2.s3.amazonaws.com"
    prefix_1 = f"{end.strftime('%Y/%m/%d')}/{site_id.upper()}/"
    prefix_2 = f"{start.strftime('%Y/%m/%d')}/{site_id.upper()}/"

    if prefix_1 == prefix_2:

        url = f"{bucket}?list-type=2&prefix={prefix_1}"
        download_url = f"{bucket}/{prefix_1}"
        
        if proxies == None:
            try:
                response = requests.get(url)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url)
                        break
                    except Exception as e:
                        i = i
        else:
            try:
                response = requests.get(url, proxies=proxies)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url)
                        break
                    except Exception as e:
                        i = i           
                        
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        
        ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        
        filenames = [
            contents.find("s3:Key", ns).text.split("/")[-1]
            for contents in root.findall("s3:Contents", ns)
        ]
        
        files = []
        for file in filenames:
            if '_MDM' not in file:
                files.append(file)
        
        files.reverse()
        if mode == 'precipitation':
            start_index = 10 * hours
        else:
            start_index = 7 * hours
        queried_files = []
        if start_index > len(files):
            start_index = len(files)
        else:
            pass
        try:
            for i in range(0, (start_index + 1), 1):
                queried_files.append(files[i])
        except Exception as e:
            for i in range(0, start_index, 1):
                queried_files.append(files[i])
            
        data = []
        data.append(download_url)
        data.append(queried_files)
        
    else:
        url_1 = f"{bucket}?list-type=2&prefix={prefix_1}"
        download_url_1 = f"{bucket}/{prefix_1}"
        
        if proxies == None:
            try:
                response = requests.get(url_1)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url_1)
                        break
                    except Exception as e:
                        i = i
        else:
            try:
                response = requests.get(url_1, proxies=proxies)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url_1)
                        break
                    except Exception as e:
                        i = i      
                        
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        
        ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        
        filenames_1 = [
            contents.find("s3:Key", ns).text.split("/")[-1]
            for contents in root.findall("s3:Contents", ns)
        ]
        
        files_1 = []
        for file in filenames_1:
            if '_MDM' not in file:
                files_1.append(file)
        
        url_2 = f"{bucket}?list-type=2&prefix={prefix_2}"
        download_url_2 = f"{bucket}/{prefix_2}"
        
        if proxies == None:
            try:
                response = requests.get(url_2)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url_2)
                        break
                    except Exception as e:
                        i = i
        else:
            try:
                response = requests.get(url_2, proxies=proxies)
            except Exception as e:
                for i in range(0, 10, 1):
                    time.sleep(60)
                    try:
                        response = requests.get(url_2)
                        break
                    except Exception as e:
                        i = i    

        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        
        ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        
        filenames_2 = [
            contents.find("s3:Key", ns).text.split("/")[-1]
            for contents in root.findall("s3:Contents", ns)
        ]
        
        files_2 = []
        for file in filenames_2:
            if '_MDM' not in file:
                files_2.append(file) 

        files_1.reverse()
        if mode == 'precipitation':
            start_index_1 = 10 * hours
        else:
            start_index_1 = 7 * hours
        queried_files_1 = []
        if start_index_1 > len(files_1):
            start_index_1 = len(files_1)
        else:
            pass
        try:
            for i in range(0, (start_index_1 + 1), 1):
                queried_files_1.append(files_1[i])
        except Exception as e:
            for i in range(0, start_index_1, 1):
                queried_files_1.append(files_1[i])

        files_2.reverse()
        hrs = 24 - start.hour
        if mode == 'precipitation':
            start_index_2 = 10 * hrs
        else:
            start_index_2 = 7 * hrs
        queried_files_2 = []
        if start_index_2 > len(files_2):
            start_index_2 = len(files_2)
        else:
            pass
        try:
            for i in range(0, (start_index_2 + 1), 1):
                queried_files_2.append(files_2[i])
        except Exception as e:
            for i in range(0, start_index_2, 1):
                queried_files_2.append(files_2[i])

        data = []
        data.append(download_url_1)
        data.append(queried_files_1)
        data.append(download_url_2)
        data.append(queried_files_2)
        
    return data