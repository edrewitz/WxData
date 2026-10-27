---
title: ECMWF High Resolution IFS Wave
---
[***Return To WxData Wiki Main Page***](https://github.com/edrewitz/WxData/wiki)
# ECMWF High Resolution IFS Wave

```python
def ecmwf_high_res_ifs_wave(final_forecast_hour=360,
                    western_bound=-180,
                    eastern_bound=180,
                    northern_bound=90,
                    southern_bound=-90,
                    step=3,
                    proxies=None,
                    process_data=True,
                    clear_recycle_bin=False,
                    custom_directory=None,
                    notifications='off',
                    source='ecmwf',
                    clear_data=False,
                    variables=['mean zero-crossing wave period',
                               'significant wave height',
                                'mean wave direction',
                                'mean wave period',
                                'peak wave period'],
                to_netcdf=False,
                netcdf_path=f"ECMWF High Resolution IFS WAVE/NETCDF",
                netcdf_filename=f"ecmwf_high_res_ifs_wave.nc",
                delete_previous_netcdf_file=True,
                return_values=True):
```
This function is the main client that downloads and processes ECMWF High Resolution IFS Wave data. 

***This client can do the following:***

1) Download ECMWF High Resolution IFS Wave data from ECMWF Open-Data, Amazon Web Services and Google Cloud servers.

2) Query your download by downloading only the variables and levels needed. 

3) Subset the GRIB data into a user-specified bounding box and decode the GRIB2 keys into plain-language.
    
4) Convert the xarray.array of decoded GRIB2 data into a NETCDF (.nc) file. 

5) Manages the ECMWF High Resolution IFS Wave files in the local directory.    

6) Handle user-specified proxy-server protocol - Useful for users working on VPN connections and behind firewalls.  

7) Automatically Rotate between ECMWF Open-Data, Amazon Web Services and Google Cloud in the event of significant server connection issues.

8) Validates the download and helps the user troubleshoot if needed. 

These ECMWF end-to-end clients can download ECMWF data from the following sources: 

    i) ECMWF Open-Data Server
    
    ii) Amazon AWS Server
    
    iii) Google Cloud Server
        
***If the server of your choice is down, the client will rotate to another one and try scanning for data and downloading there.***
***If the client cannot connect to any of the servers, the system will exit.***

1) final_forecast_hour (Integer) - Default = 360.

***00z and 12z ECMWF High Resolution IFS Wave Runs***

3-Hourly Increments from hour 0 to hour 144.

6-Hourly Increments from hour 144 to hour 360

***06z and 18z ECMWF High Resolution IFS Wave Runs***

3-Hourly Increments from hour 0 to hour 144.  

2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

6) step (Integer) - Default=3. The time increment of the data. Options are 3hr and 6hr. 

7) proxies (dict or None) - Default=None. If the user is using proxy server(s), the user must change the following:

  ```python
   proxies=None ---> proxies={
                           'http':'http://your-proxy-address:port',
                           'https':'http://your-proxy-address:port'
                           }
  ```

8) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
   data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
   
9) clear_recycle_bin (Boolean) - (Default=False). Set to True to clear your recycle bin. 
    
10) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
    either Celsius or Fahrenheit. When False, this data remains in Kelvin.
    
11) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
    Set convert_to='fahrenheit' for Fahrenheit. 
    
12) custom_directory (String or None) - Default=None. The directory path where the ECMWF IFS Wave files will be saved to.
    Default = "ECMWF/IFS/HIGH RES WAVE"

13) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}

14) source (String) - Default='ecmwf'. The data server choice. 

    ***Data Sources***
    
     i) ECMWF Open-Data Server = 'ecmwf'
     
     i) Amazon AWS Server = 'aws'
      
     iii) Google Cloud Server = 'google'
   
  *If the client is unable to connect to the server the user specified, it will rotate to the next server and try to 
  establish a connection there.*
    
15) clear_data (Boolean) - Default=False. When set to False, the scanner safe-guard remains in place (recommended for most users).
    When set to True, the scanner safe-guard is disabled and directory branch is cleared and new data is downloaded. 

16) variables (String List) - Default is all variables. The list of variable names in plain-language. 

    ***Variables***

    ```python
    'mean zero-crossing wave period'
    'significant wave height'
    'mean wave direction'
    'mean wave period'
    'peak wave period'
    ```
    
17) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.

18) netcdf_path (String) - Default='ECMWF High Resolution IFS WAVE/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.

19) netcdf_filename (String) - Default='ecmwf_high_res_ifs_wave.nc'. The name of the netCDF (.nc) file. A good practice is to 
    name this netCDF file using the variable name. 
    
20) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
    new netCDF file. For users who want to archive all data set this to False. 
    
21) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
    
**Returns**

An xarray.data array with post-processed GRIB2 Variable Keys into Plain Language Variable Keys

***Plain Language ECMWF High Resolution IFS Wave Variable Keys (After Post-Processing)***

```python
'mean_zero_crossing_wave_period'
'significant_height_of_combined_waves_and_swell'
'mean_wave_direction'
'peak_wave_period'
'mean_wave_period'
```
