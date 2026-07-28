# Byte-Range Request

***def byte_range_request(grib_url,
                      idx_url,
                      variables,
                      levels,
                      level_type,
                      path,
                      filename,
                      proxies=None,
                      chunk_size=1024,
                      notifications='on',
                      clear_recycle_bin=False):***

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
    
    4) clear_recycle_bin (Boolean) - (Default=False in WxData >= 1.2.5) (Default=True in WxData < 1.2.5). When set to True, 
        the contents in your recycle/trash bin will be deleted with each run of the program you are calling WxData. 
        This setting is to help preserve memory on the machine. 
        
    Returns
    -------
    
    Downloads a partial GRIB file consisting of the variable the user specifies.     
