# NOAA/NWS Climate Prediction Center Outlooks

***def get_cpc_outlook(parameter,
                    path,
                    filename,
                    proxies=None,
                    chunk_size=8192,
                    notifications='on',
                    clear_recycle_bin=False,
                    file_extension='.zip',
                    crs='EPSG:4326'):***

    This function will download the shapefiles for the latest NOAA Climate Prediction Center Outlook and return a clean geopandas.GeoDataFrame of the data
    
    Required Arguments:
    
    1) parameter (String) - The type of CPC Outlook.
    
        Parameter List
        --------------
        
        1) '6_10_day_precipitation'
        2) '6_10_day_temperature'
        3) '8_14_day_precipitation'
        4) '8_14_day_temperature'
        5) 'week_3_4_precipitation'
        6) 'week_3_4_temperature'
        7) 'monthly_precipitation'
        8) 'monthly_temperature'
        
    2) path (String) - The local directory where the CPC Outlook Shapefiles will download to
    
    3) filename (String) - The filename the user wants to save the CPC Outlook as
    
    Optional Arguments:
    
    1) proxies (dict or None) - Default=None. If the user is using a proxy server, the user must change the following:

        proxies=None ---> proxies={'http':'http://url',
                            'https':'https://url'
                            }
        
    2) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    3) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    4) clear_recycle_bin (Boolean) - When set to True, the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
          This setting is to help preserve memory on the machine. 
          
    5) file_extension (String) - Default='.zip'. - The extension of the zip file. 
    
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    6) crs (String) - Default='EPSG:4326' (ccrs.PlateCarree()) - The coordinate reference system the user wants the geometry coordinates in.  
    
    Returns
    -------
    
    A geopandas.GeoDataFrame of the calibrated CPC Probabilistic Forecast Data 
