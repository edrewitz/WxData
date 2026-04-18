# WxData

<img src="https://github.com/edrewitz/WxData/blob/main/icons/weather%20icon.jpg?raw=true" width="200" alt="Alt text" /> <img src="https://github.com/edrewitz/WxData/blob/1be590e9a16033974a592d8cf99f3cd521f95e0b/icons/python%20logo.png?raw=true" width="200" alt="Alt text" />

[![Conda Recipe](https://img.shields.io/badge/recipe-wxdata-green.svg)](https://anaconda.org/conda-forge/wxdata) [![Conda Version](https://img.shields.io/conda/vn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) ![PyPI](https://img.shields.io/pypi/v/wxdata?label=pypi%20wxdata) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/license.svg)](https://anaconda.org/conda-forge/wxdata) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/wxdata) 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17727621.svg)](https://doi.org/10.5281/zenodo.17727621)



Anaconda Downloads

[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata)


PIP Downloads:

![PyPI - Downloads](https://img.shields.io/pypi/dm/wxdata)



**(C) Eric J. Drewitz 2025-2026**

A Python package consisting of the following:

1) End-to-end weather data clients with VPN/PROXY support
2) Raw data clients with VPN/PROXY support
3) Data processors that decode variable keys from GRIB format into a plain-language format
4) Various tools for assisting Python automated workflows, querying meteorological datasets and filling gaps in meteorological data.

# Table of Contents

1) [Installation Instructions](https://github.com/edrewitz/WxData?tab=readme-ov-file#installation-instructions)
2) [Proxy Server Configuration](https://github.com/edrewitz/WxData?tab=readme-ov-file#proxy-server-configuration)
3) [What makes WxData unique among various meteorological Python packages?](https://github.com/edrewitz/WxData?tab=readme-ov-file#what-makes-wxdata-unique-among-various-meteorological-python-packages)
4) [WxData Tutorials](https://github.com/edrewitz/WxData?tab=readme-ov-file#wxdata-tutorials)
5) [WxData Documentation](https://github.com/edrewitz/WxData?tab=readme-ov-file#wxdata-documentation)
6) [Importing Functions from WxData](https://github.com/edrewitz/WxData?tab=readme-ov-file#importing-functions-from-wxdata)
7) [Citations](https://github.com/edrewitz/WxData?tab=readme-ov-file#citations)
8) [Data Sources](https://github.com/edrewitz/WxData?tab=readme-ov-file#data-sources)


## Installation Instructions

**How To Install**

Copy and paste either command into your terminal or anaconda prompt:

*Install via Anaconda*

`conda install wxdata`

*Install via pip*

`pip install wxdata`

**How To Update To The Latest Version**

Copy and paste either command into your terminal or anaconda prompt:

*Update via Anaconda*

***This is for users who initially installed WxData through Anaconda***

`conda update wxdata`

*Update via pip*

***This is for users who initially installed WxData through pip***

`pip install --upgrade wxdata`

***Important Compatibility Information***

When a new version of Python comes out, it might not be compatible with the C++ eccodes library immediately (especially on pip/pypi versions).

This issue arises when the user is post-processing GRIB data.

There are two options to resolve this issue:

i) Install wxdata via Anaconda/Miniconda3 --> `conda install wxdata`

ii) Set up a new environment with an earlier version of Python (must be Python >= 3.10) and then `pip install wxdata`

---------------------------------------------------------

## Proxy Server Configuration

***Friendly for users working on VPN/PROXY connections***

   Depending on which client, the proxy-address:port must be entered as either a dictionary or a string.

   The clients that use a string for proxies are:

   1) All ECMWF clients.

   2) METAR Observations Client.
      
   3) `pixel_query()` tool if the user needs to download the airport station codes list.

   4) All NEXRAD II Radar Data clients.

   5) Open AWS Data Client.

      All other clients use proxies as a dictionary

                  Example: We want to download the latest Observed Sounding Data for San Diego, CA (NKX)
         
                  proxies=None ---> proxies={
                                         'http':'http://your-proxy-address:port',
                                         'https':'http://your-proxy-address:port'
                                         }
         
                  sounding_data = get_observed_sounding_data('nkx', proxies=proxies)
         
                  Example: We want to download the ECMWF IFS Data:
         
                  proxies=None ---> proxies="http://your-proxy-address:port" ---> ds = ecmwf_ifs(proxies=proxies)

<img src="https://github.com/edrewitz/WxData/blob/main/diagrams/proxy.png?raw=true" width="500" alt="Alt text" /> 


   For more information on configuring proxies: https://requests.readthedocs.io/en/latest/user/advanced/#proxies

---------------------------------------------------------------------

## What makes WxData unique among various meteorological Python packages?
       
1) Converts GRIB variable keys into variable keys that are in plain language.
    - (e.g. 'r2' ---> '2m_relative_humidity')
      
2) Has a scanner that checks if the data files on your PC are up to date with those on the data server.
   - This is a safeguard to protect newer developers from getting temporary IP address bans from the various data servers.
   - Improves performance by preventing the potential of repetative downloading the same dataset.

3) Preserves system memory via the following methods:
   - Clears out old data files before each new data download.
   - Optional setting `clear_recycle_bin` in all functions.
        - When `clear_recycle_bin=True` the computer's recycle/trash bin is cleared with each run of the script using any WxData function.
        - If a user wishes to not clear out their recycle bin `set clear_recycle_bin=False`.
        - Default: `clear_recycle_bin=False`.
    
4) Has built-in support for users on VPN/PROXY connections.

5) Consists of both observational and model data.

6) Has additional tools to assist querying data, resolving gaps in data and automating your Python workflow. 

-----------------------------------------------
    
## WxData Tutorials

*Regular Users*
1) [Downloading METAR Data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/metars.ipynb)
2) [Downloading Observed Sounding Data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/soundings.ipynb)
3) [Downloading the first 72 hours of the ECMWF IFS and ECMWF AIFS](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/ecmwf.ipynb)
4) [Downloading the GEFS members p01 and p02 for only Temperature](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/gefs.ipynb)
5) [Downloading the Real-Time Mesoscale Analysis (RTMA)](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/rtma.ipynb)
6) [Downloading the SPC Convective Outlook for CONUS](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/spc.ipynb)
7) [Downloading NWS Maximum Temperature Forecast for Hawaii](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/nws_hi.ipynb)
8) [Downloading the GFS0P25 then performing pixel and line queries on the data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/GFS.ipynb)
9) [Downloading various datasets from the Applied Climate Information System (ACIS)](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/xmacis2.ipynb)
10) [Downloading AIGFS Data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/aigfs.ipynb)
11) [Downloading AIGEFS Data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/aigefs.ipynb)
12) [Downloading and plotting the Climate Prediction Center 6-10 Day Precipitation Outlook](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/cpc_precip_outlook.ipynb)
13) [Downloading OUN Sounding Data and Using The WxData Linear Anti Aliasing Tool To Interpolate 100 Points Between Each Observed Data Point And Visualize Both Data Sets](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/linear_anti_aliasing.ipynb)
14) [Downloading Subsets Of ECMWF IFS Ensemble and AIFS Ensemble Data](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/ecmwf_ens.ipynb)
15) [Downloading the ECMWF IFS 500 mb Geopotential Height Initial Analysis And Plot A North Pole Stereographic Resolving The Meridian With The WxData Cyclic Point Tool](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/cyclic.ipynb)
16) [Downloading Observed Fuels Data For The Past Year For Acton RAWS and Plotting 1000-HR Dead Fuel Moisture](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/acton_raws.ipynb)
17) [Downloading the 7-Day NFDRS Forecast for Acton RAWS and Plotting Forecast 100-HR Dead Fuel Moisture](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/acton_raws_forecast.ipynb)
18) [Downloading Current RAWS and METAR Data and Plotting Current Relative Humidity Observations Across California and Nevada](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/metar_raws_observed_rh.ipynb)
19) [Downloading Current RAWS Data and Plotting Current Energy Release Components (ERCs) Observations Across California and Nevada](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/observed_erc_map.ipynb)

*Advanced Users*
1) [Using the `client` module to download the latest HadCRUT5 Analysis netCDF file and open this dataset in xarray](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/hadcrut5.ipynb)
2) [Downloading the GFS0P25 for temperature fields and using run_external_scripts() to post-process this GFS0P25 dataset in an external Python script](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/external_scripts.ipynb)

---------------------------------------------------

## WxData Documentation

***Documentation Sections***

1. [End-To-End Data Clients](https://github.com/edrewitz/WxData?tab=readme-ov-file#end-to-end-data-clients)
2. [Raw Data Clients](https://github.com/edrewitz/WxData?tab=readme-ov-file#raw-data-clients)
3. [Post-Processors](https://github.com/edrewitz/WxData?tab=readme-ov-file#post-processors)
4. [Data Querying Tools](https://github.com/edrewitz/WxData?tab=readme-ov-file#data-querying-tools)
5. [Data Transformation & Gap Filling Tools](https://github.com/edrewitz/WxData?tab=readme-ov-file#data-transformation--gap-filling-tools)
6. [Automated Python Workflow Tools](https://github.com/edrewitz/WxData?tab=readme-ov-file#automated-python-workflow-tools)

### End-To-End Data Clients

***Global Forecast System (GFS)***
1. [GFS0P25](https://github.com/edrewitz/WxData/blob/main/Documentation/GFS0P25.md)
2. [GFS0P25 SECONDARY PARAMETERS](https://github.com/edrewitz/WxData/blob/main/Documentation/GFS0P25%20Secondary%20Parameters.md)
3. [GFS0P50](https://github.com/edrewitz/WxData/blob/main/Documentation/GEFS0P50.md)

***AI Global Forecast System (AIGFS)***
1. [AIGFS](https://github.com/edrewitz/WxData/blob/main/Documentation/aigfs.md)

***Climate Forecast System (CFS)***
1. [CFS Pressure](https://github.com/edrewitz/WxData/blob/main/Documentation/cfs_pressure.md#climate-forecast-system-cfs-pressure)
2. [CFS Flux](https://github.com/edrewitz/WxData/blob/main/Documentation/cfs_flux.md#climate-forecast-system-cfs-flux)

***Hybrid Global Ensemble Forecast System (HGEFS)***
1. [HGEFS](https://github.com/edrewitz/WxData/blob/main/Documentation/hgefs.md#hybrid-global-ensemble-forecast-system-hgefs)

***Global Ensemble Forecast System (GEFS)***
1. [GEFS0P50](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P50.md#global-ensemble-forecast-system-050-x-050-degree-gefs0p50)
2. [GEFS0P50 SECONDARY PARAMETERS](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P50%20Secondary%20Parameters.md#global-ensemble-forecast-system-050-x-050-degree-secondary-parameters-gefs0p50-secondary-parameters)
3. [GEFS0P25](https://github.com/edrewitz/wxdata/blob/main/Documentation/GEFS0P25.md#global-ensemble-forecast-system-025-x-025-degree-gefs0p25)

***AI Global Ensemble Forecast System (AIGEFS)***
1. [AIGEFS Members (Pressure Parameters)](https://github.com/edrewitz/WxData/blob/main/Documentation/aigefs_pressure_members.md)
2. [AIGEFS Members (Surface Parameters)](https://github.com/edrewitz/WxData/blob/main/Documentation/aigefs_surface_members.md)
3. [AIGEFS Ensemble Mean & Ensemble Spread](https://github.com/edrewitz/WxData/blob/main/Documentation/aigefs_single.md)

***ECMWF Open Data***
1. [ECMWF IFS](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF_IFS.md)
2. [ECMWF IFS Ensemble](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20IFS%20Ensemble.md#ecmwf-ifs-ensemble)
3. [ECMWF AIFS](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF_AIFS.md)
4. [ECMWF AIFS Ensemble](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20AIFS%20Ensemble.md#ecmwf-aifs-ensemble)
5. [ECMWF IFS Wave](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF_IFS_Wave.md)
6. [ECMWF IFS Wave Ensemble](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20IFS%20Wave%20Ensemble.md#ecmwf-ifs-wave-ensemble)
   
***Real-Time Mesoscale Analysis (RTMA)***
1. [RTMA](https://github.com/edrewitz/wxdata/blob/main/Documentation/rtma.md#real-time-mesoscale-analysis-rtma)
2. [RTMA Comparison](https://github.com/edrewitz/wxdata/blob/main/Documentation/rtma%20comparison.md#real-time-mesoscale-analysis-rtma-24-hour-comparison)

***NOAA Storm Prediction Center Outlooks/Climate Prediction Center Outlooks/National Weather Service Forecasts***
1. [Get NDFD Grids](https://github.com/edrewitz/wxdata/blob/main/Documentation/noaa.md#noaa-get-storm-prediction-center-outlooks-and-national-weather-service-forecasts-ndfd-grids)
2. [Climate Prediction Center Outlooks](https://github.com/edrewitz/WxData/blob/main/Documentation/cpc_outlooks.md#noaanws-climate-prediction-center-outlooks)

***METAR Observations***
1. [METAR Observations](https://github.com/edrewitz/wxdata/blob/main/Documentation/metars.md#metar-observations)

***FEMS RAWS Network***
1. [Get Single Station Weather Observations](https://github.com/edrewitz/WxData/blob/main/Documentation/single%20raws%20weather%20obs.md#fems-single-raws-station-weather-observations)
2. [Get Single Station Fuels Observations](https://github.com/edrewitz/WxData/blob/main/Documentation/single%20raws%20fuels%20obs.md#fems-single-raws-station-fuels-observations)
3. [Get Multi Station Weather Observations](https://github.com/edrewitz/WxData/blob/main/Documentation/multi%20raws%20weather%20obs.md#fems-multi-raws-station-weather-observations)
4. [Get Multi Station Fuels Observations](https://github.com/edrewitz/WxData/blob/main/Documentation/multi%20raws%20fuels%20obs.md#fems-multi-raws-station-fuels-observations)
5. [Get Current Multi Station Weather Observations](https://github.com/edrewitz/WxData/blob/main/Documentation/current%20multi%20raws%20weather%20obs.md#fems-multi-raws-station-current-weather-observations)
6. [Get Current Multi Station Fuels Observations](https://github.com/edrewitz/WxData/blob/main/Documentation/current%20multi%20raws%20fuels%20obs.md#fems-multi-raws-station-current-fuels-observations)
7. [Get Current Multi Station Weather Observations By State](https://github.com/edrewitz/WxData/blob/main/Documentation/raws%20weather%20obs%20by%20state.md#fems-raws-station-current-weather-observations-by-state)
8. [Get Current Multi Station Fuels Observations By State](https://github.com/edrewitz/WxData/blob/main/Documentation/raws%20fuels%20obs%20by%20state.md#fems-raws-station-current-fuels-observations-by-state)
9. [Get Single Station Weather Forecast](https://github.com/edrewitz/WxData/blob/main/Documentation/single%20raws%20weather%20forecast.md#fems-single-raws-station-weather-forecast)
10. [Get Single Station NFDRS (Fuels) Forecast](https://github.com/edrewitz/WxData/blob/main/Documentation/single%20raws%20nfdrs%20forecast.md#fems-single-raws-station-nfdrs-fuels-forecast)
11. [Get Multi Station Weather Forecast](https://github.com/edrewitz/WxData/blob/main/Documentation/multi%20raws%20weather%20forecast.md#fems-multi-raws-station-weather-forecast)
12. [Get Multi Station NFDRS (Fuels) Forecast](https://github.com/edrewitz/WxData/blob/main/Documentation/multi%20raws%20nfdrs%20forecast.md#fems-multi-raws-station-nfdrs-fuels-forecast)
13. [Get Single Station Meta-Data](https://github.com/edrewitz/WxData/blob/main/Documentation/raws%20single%20station%20meta%20data.md#fems-single-raws-station-meta-data)
14. [Get Multi Station Meta-Data](https://github.com/edrewitz/WxData/blob/main/Documentation/raws%20multi%20station%20meta%20data.md#fems-multi-raws-station-meta-data)

***Observed Atmospheric Soundings***
1. [University Of Wyoming Soundings](https://github.com/edrewitz/wxdata/blob/main/Documentation/wyoming_soundings.md)

***NEXRAD II Radar Data***
1. [Single Site](https://github.com/edrewitz/WxData/blob/main/Documentation/nexrad2_single.md#nexrad-ii-single-radar)
2. [Multi-Site](https://github.com/edrewitz/WxData/blob/main/Documentation/nexrad2_multi.md#nexrad-ii-multi-radar)

-----------------------------

### Post-Processors

***GFS Post-Processing***
1. [Primary GFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Primary%20GFS%20Post%20Processing.md)
2. [Secondary GFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Secondary%20GFS%20Post%20Processing.md)

***AIGFS Post-Processing***
1. [AIGFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/aigfs_post_processing.md)

***CFS Post-Processing***
1. [CFS Pressure Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/cfs_pressure_post_processing.md#climate-forecast-system-cfs-pressure-post-processing)
2. [CFS Flux Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/cfs_flux_post_processing.md#climate-forecast-system-cfs-flux-post-processing)

***GEFS Post-Processing***
1. [Primary GEFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Primary%20GEFS%20Post-Processing.md)
2. [Secondary GEFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/Secondary%20GEFS%20Post%20Processing.md)

***AIGEFS Post-Processing***
1. [AIGEFS Members Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/aigefs_members_post_processing.md)
2. [AIGEFS Single Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/aigefs_single_post_processing.md)

***HGEFS Post-Processing***
1. [HGEFS Post-Processing](https://github.com/edrewitz/WxData/blob/main/Documentation/hgefs_post_processing.md#hybrid-global-ensemble-forecast-system-hgefs-post-processing)

***ECMWF Post-Processing***
1. [ECMWF IFS and IFS Ensemble](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20IFS%20Post%20Processing.md#ecmwf-ifs-and-ifs-ensemble-post-processing)
2. [ECMWF AIFS and AIFS Ensemble](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20AIFS%20Post%20Processing.md#ecmwf-aifs-and-aifs-ensemble-post-processing)
3. [ECMWF IFS Wave and IFS Wave Ensemble](https://github.com/edrewitz/WxData/blob/main/Documentation/ECMWF%20IFS%20Wave%20Post%20Processing.md#ecmwf-ifs-wave-and-ifs-wave-ensemble-post-processing)

***Real-Time Mesoscale Analysis Post-Processing***
1. [RTMA](https://github.com/edrewitz/WxData/blob/main/Documentation/RTMA%20Post%20Processing.md)

-----------------------------------------------

### Raw Data Clients

***xmACIS2 Climate Data***
1. [xmACIS2 Client](https://github.com/edrewitz/WxData/blob/main/Documentation/xmacis2_client.md)

***Custom Gridded Data***
1. [Gridded Data Client](https://github.com/edrewitz/WxData/blob/main/Documentation/get_gridded_data.md#get-gridded-data)

***Custom CSV Data***
1. [CSV Data Client](https://github.com/edrewitz/WxData/blob/main/Documentation/get_csv_data.md#get-csv-data)

***Custom Excel Data***
1. [Excel Data Client](https://github.com/edrewitz/WxData/blob/main/Documentation/get_excel_data.md#get-excel-data)

***AWS Open Data***
1. [AWS Open Data](https://github.com/edrewitz/WxData/blob/main/Documentation/get_open_aws_data.md#get-aws-open-data)

---------------------------------------------------------------

### Data Querying Tools

***Pixel Query***
1. [pixel_query](https://github.com/edrewitz/WxData/blob/main/Documentation/pixel_query.md)

***Line Query***
1. [line_query](https://github.com/edrewitz/WxData/blob/main/Documentation/line_query.md)

--------------------------------------------------

### Data Transformation & Gap Filling Tools

***Cyclic Points For Hemispheric Plots***
1. [Cyclic Points](https://github.com/edrewitz/wxdata/blob/main/Documentation/cyclic_point.md#using-wxdata-to-add-cyclic-points-for-hemispheric-plots)

***Shifting Longitude From 0 to 360 --> -180 to 180***
1. [shift_longitude](https://github.com/edrewitz/WxData/blob/main/Documentation/shift_longitude.md)

***Linear Anti-Aliasing Between Two Points***
1. [linear_anti_aliasing](https://github.com/edrewitz/WxData/blob/main/Documentation/linear_anti_aliasing.md#linear-anti-aliasing-between-points)

------------------------------------------

### Automated Python Workflow Tools

***Running External Python Scripts In Your Workflow***

1 [run_external_scripts](https://github.com/edrewitz/WxData/blob/main/Documentation/run_external_scripts.md)

---------------------------------------

## Importing Functions from WxData

      """
      This file hosts all of the functions in the WxData Python library that directly interact with the user. 
      
      (C) Eric J. Drewitz 2025-2026
      """
      
      
      """
      This section of functions are for users who want full wxdata functionality.
      
      These functions do the following:
      
      1) Scan for the latest available data. 
          - If the data on your local machine is not up to date, new data will download automatically.
          - If the data on your local machine is up to date, new data download is bypassed.
          - This is a safeguard that prevents excessive requests on the data servers.
          
      2) Builds the wxdata directory to store the weather data files. 
          - Scans for the directory branch and builds the branch if it does not exist. 
      
      3) Downloads the data.
          - Users can define their VPN/PROXY IP Address as a (dict) in their script and pass their
            VPN/PROXY IP address into the function to avoid SSL Certificate errors when requesting data.
          - Algorithm allows for up to 5 retries with a 30 second break between each retry to resolve connection
            interruptions while not overburdening the data servers. 
      
      4) Pre-processes the data via filename formatting and correctly filing in the wxdata directory. 
      
      5) Post-processing by doing the following tasks:
           - Remapping GRIB2 variable keys into plain language variable keys.
           - Fixing dataset build errors and grouping all variables together.
           - Transforms longitude from 0 to 360 degrees into -180 to 180 degrees.
           - Subsetting the data to the latitude/longitude boundaries specified by the user. 
           - Converting temperature from kelvin to units the user wants (default is Celsius).
           - Returning a post-processed xarray.array to the user. 
           
      6) Preserves system memory by doing the following:
           - Deleting old data files before each new download.
           - When clear_recycle_bin=True, the user's recycle bin is also cleared. 
      """
      
      # Global Forecast System (GFS)
      # - GFS 0.25x0.25 Degree Primary Parameters
      # - GFS 0.25x0.25 Degree Secondary Parameters
      # - GFS 0.5x0.5 Degree
      from wxdata.gfs.gfs import(
          gfs_0p25,
          gfs_0p25_secondary_parameters,
          gfs_0p50
      )
      
      # AI Global Forecast System (AIGFS)
      from wxdata.aigfs.aigfs import aigfs
      
      # Hybrid Global Ensemble Forecast System (HGEFS)
      from wxdata.hgefs.hgefs import hgefs_mean_spread
      
      # Global Ensemble Forecast System (GEFS)
      # - GEFS 0.5x0.5 Degree Primary Parameters
      # - GEFS 0.5x0.5 Degree Secondary Parameters
      # - GEFS 0.25x0.25 Degree
      from wxdata.gefs.gefs import(
          gefs_0p50,
          gefs_0p50_secondary_parameters,
          gefs_0p25
      )
      
      # Climate Forecast System (CFS)
      # - CFS Flux Products
      # - CFS Pressure Products
      from wxdata.cfs.cfs import(
          cfs_flux,
          cfs_pressure
      )
      
      # AI Global Ensemble Forecast System (AIGEFS)
      # - AIGEFS Pressure Members (Pressure Level Variables)
      # - AIGEFS Surface Members (Surface Level Variables)
      # - AIGEFS Single (AIGEFS Ensemble Mean & AIGEFS Ensemble Spread)
      from wxdata.aigefs.aigefs import(
          aigefs_pressure_members,
          aigefs_surface_members,
          aigefs_single
      )
      
      # European Centre for Medium-Range Weather Forecasts (ECMWF)
      # - ECMWF IFS
      # - ECMWF IFS Ensemble
      # - ECMWF AIFS
      # - ECMWF AIFS Ensemble
      # - ECMWF IFS Wave
      # - ECMWF IFS Wave Ensemble
      from wxdata.ecmwf.ecmwf import(
          ecmwf_ifs,
          ecmwf_ifs_ens,
          ecmwf_aifs,
          ecmwf_aifs_ens,
          ecmwf_ifs_wave,
          ecmwf_ifs_wave_ens
      )
      
      # FEMS RAWS Network
      # - Single Station Weather Observations
      # - Single Station Fuels Observations
      # - Multi Station Weather Observations
      # - Multi Station Fuels Observations
      # - Current Weather Observations - Multi Station
      # - Current Fuels Observations - Multi Station
      # - Current Weather Observations - All Stations By State
      # - Current Fuels Observations - All Stations By State
      # - Single Station NFDRS Forecast
      # - Multi Station NFDRS Forecast
      # - Single Station Weather Forecast
      # - Multi Station Weather Forecast
      from wxdata.fems.observations import(
          get_single_raws_station_weather_observations,
          get_single_raws_station_fuels_observations,
          get_multi_raws_station_weather_observations,
          get_multi_raws_station_fuels_observations,
          get_current_multi_raws_station_weather_observations,
          get_current_multi_raws_station_fuels_observations,
          get_current_all_raws_station_weather_observations,
          get_current_all_raws_station_fuels_observations,
          get_single_raws_station_nfdrs_forecast,
          get_multi_raws_station_nfdrs_forecast,
          get_single_raws_station_weather_forecast,
          get_multi_raws_station_weather_forecast
      )
      
      # FEMS RAWS Network
      # - Single Station Meta Data
      # - Multi Station Meta Data
      from wxdata.fems.meta_data import(
          get_single_raws_station_meta_data,
          get_multi_raws_station_meta_data
      )
      
      # Real-Time Mesoscale Analysis (RTMA)
      # - RTMA Latest
      # - RTMA Comparison Between Two Times
      from wxdata.rtma.rtma import(
          rtma, 
          rtma_comparison
      )
      
      # NOAA 
      # - Storm Prediction Center Outlooks
      # - Climate Prediction Center Outlooks
      # - National Weather Service Forecasts
      from wxdata.noaa.nws import(
          get_ndfd_grids,
          get_cpc_outlook
      )
      
      # Observed Upper-Air Soundings
      # (University of Wyoming Database)
      from wxdata.soundings.wyoming_soundings import get_observed_sounding_data
      
      # METAR Observational Data (From NOAA)
      from wxdata.metars.metar_obs import download_metar_data
      
      # NEXRAD2 Radar Data
      # - NEXRAD2 Radar Single Station
      # - NEXRAD2 Radar Multi Station
      from wxdata.radar.nexrad2 import(
          download_current_single_station_nexrad2_radar_data,
          download_current_multi_station_nexrad2_radar_data
      )
      
      """
      This section hosts all the functions and modules that involve post-processing the data.
      These are the functions and modules that:
      
      1) Re-map the GRIB2 Variable Keys into Plain Language Keys
      2) Build the xarray.array of the various datasets. 
      
      """
      
      
      # Global Forecast System (GFS)
      import wxdata.post_processors.gfs_post_processing as gfs_post_processing
      
      # AI Global Forecast System (AIGFS)
      import wxdata.post_processors.aigfs_post_processing as aigfs_post_processing
      
      # Hybrid Global Ensemble Forecast System (HGEFS)
      import wxdata.post_processors.hgefs_post_processing as hgefs_post_processing
      
      # Global Ensemble Forecast System (GEFS)
      import wxdata.post_processors.gefs_post_processing as gefs_post_processing
      
      # AI Global Ensemble Forecast System (AIGEFS)
      import wxdata.post_processors.aigefs_post_processing as aigefs_post_processing
      
      # European Centre for Medium-Range Weather Forecasts (ECMWF)
      import wxdata.post_processors.ecmwf_post_processing as ecmwf_post_processing
      
      # Climate Forecast System (CFS)
      import wxdata.post_processors.cfs_post_processing as cfs_post_processing
      
      # Real-Time Mesoscale Analysis (RTMA)
      from wxdata.post_processors.rtma_post_processing import process_rtma_data
      
      
      """
      This section hosts the utility functions accessable to the user. 
      
      These functions provide helpful utilities when analyzing weather data. 
      
      Utility functions are geared towards the following types of users:
      
      1) Users who want to use their own scripts to download the data however, they
         would like to use the wxdata post-processing capabilities. 
         
      2) Users who want to make hemispheric graphics or any graphics where cyclic points
         resolve missing data along the prime meridian or international dateline. 
      """
      # WxData function using cartopy to make cyclic points
      # This is for users who wish to make graphics that cross the -180/180 degree longitude line
      # This is commonly used for Hemispheric graphics
      # Function that converts the longitude dimension in an xarray.array 
      # From 0 to 360 to -180 to 180
      from wxdata.utils.coords import(
          cyclic_point,
          shift_longitude
      )
      
      # Functions to pixel query and query pixels along a line between points A and B
      # Function to interpolate to n amount of points in between x and y values respectively
      from wxdata.utils.tools import(
          pixel_query,
          line_query,
          linear_anti_aliasing
      )
      
      # This function executes a list of Python scripts in the order the user lists them
      from wxdata.utils.scripts import run_external_scripts
      
      """
      This section hosts the various data clients that retrieve various types of data.
      
      These clients can be easily configured to work on VPN/PROXY connections.
      """
      
      # These are the wxdata HTTPS Clients with full VPN/PROXY Support
      # Client List:
      #  - get_gridded_data()
      #  - get_csv_data()
      #  - get_excel_data()
      #  - get_xmacis_data()
      #  - get_open_aws_data()
      import wxdata.client.client as client

-------------------------------------------

## Citations

**MetPy**: May, R. M., Goebbert, K. H., Thielen, J. E., Leeman, J. R., Camron, M. D., Bruick, Z.,
    Bruning, E. C., Manser, R. P., Arms, S. C., and Marsh, P. T., 2022: MetPy: A
    Meteorological Python Library for Data Analysis and Visualization. Bull. Amer. Meteor.
    Soc., 103, E2273-E2284, https://doi.org/10.1175/BAMS-D-21-0125.1.

**xarray**: Hoyer, S., Hamman, J. (In revision). Xarray: N-D labeled arrays and datasets in Python. Journal of Open Research Software.

**cartopy**: Phil Elson, Elliott Sales de Andrade, Greg Lucas, Ryan May, Richard Hattersley, Ed Campbell, Andrew Dawson, Bill Little, Stephane Raynaud, scmc72, Alan D. Snow, Ruth Comer, Kevin Donkers, Byron Blay, Peter Killick, Nat Wilson, Patrick Peglar, lgolston, lbdreyer, … Chris Havlin. (2023). SciTools/cartopy: v0.22.0 (v0.22.0). Zenodo. https://doi.org/10.5281/zenodo.8216315

**NumPy**: Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2. (Publisher link).

**Pandas**: Pandas: McKinney, W., & others. (2010). Data structures for statistical computing in python. In Proceedings of the 9th Python in Science Conference (Vol. 445, pp. 51–56).

**dask**: Dask Development Team (2016). Dask: Library for dynamic task scheduling. URL http://dask.pydata.org

**cfgrib**: Author: ECMWF, Year: (2025), Title: cfgrib: A Python interface to map GRIB files to xarray, Source: https://github.com/ecmwf/cfgrib 

**requests**: K. Reitz, "Requests: HTTP for Humans". Available: https://requests.readthedocs.io/.

**Beautiful Soup**: Richardson, L. (2025). Beautiful Soup (Version 4.14.3) [Computer software]. https://www.crummy.com/software/BeautifulSoup/

**shapeography**: Eric J. Drewitz. (2026). edrewitz/shapeography: shapeography 1.0 Released (shapeography1.0). Zenodo. https://doi.org/10.5281/zenodo.18676845

**geopandas**: Kelsey Jordahl, Joris Van den Bossche, Martin Fleischmann, Jacob Wasserman, James McBride, Jeffrey Gerard, … François Leblanc. (2020, July 15). geopandas/geopandas: v0.8.1 (Version v0.8.1). Zenodo. http://doi.org/10.5281/zenodo.3946761

**tqdm**: da Costa-Luis, (2019). tqdm: A Fast, Extensible Progress Meter for Python and CLI. Journal of Open Source Software, 4(37), 1277, https://doi.org/10.21105/joss.01277

**ecmwf-opendata**: European Centre for Medium-Range Weather Forecasts (2026). ecmwf-opendata[Computer software]. GitHub. https://github.com/ecmwf/ecmwf-opendata

**openpyxl**: Gazoni, E., & Clark, C. (2024). openpyxl: A Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files (Version 3.1.5) [Computer software]. https://openpyxl.readthedocs.io/

**pyart**: Helmus, J.J. & Collis, S.M., (2016). The Python ARM Radar Toolkit (Py-ART), a Library for Working with Weather Radar Data in the Python Programming Language. Journal of Open Research Software. 4(1), p.e25. DOI: 10.5334/jors.119.

----------------------------------------------------------

## Data Sources

1) [National Oceanic and Atmospheric Administration/National Center for Environmental Prediction](https://nomads.ncep.noaa.gov/)
2) [European Centre for Medium-Range Weather Forecasts](https://data.ecmwf.int/forecasts/)
3) [University of Wyoming](http://www.weather.uwyo.edu/upperair/sounding.shtml)
4) [National Oceanic and Atmospheric Administration/National Weather Service](https://tgftp.nws.noaa.gov/)
5) [National Oceanic and Atmospheric Administration/Aviation Weather Center](https://aviationweather.gov/)
6) [National Oceanic and Atmospheric Administration/Climate Prediction Center](https://www.cpc.ncep.noaa.gov/products/GIS/GIS_DATA/us_tempprcpfcst/index.php)
7) [Applied Climate Information System (ACIS)](https://www.rcc-acis.org/docs_webservices.html)
8) [USDA Fire Environment Mapping System](https://fems.fs2c.usda.gov/download)
9) [Amazon AWS Unidata NEXRAD2 Bucket](https://unidata-nexrad-level2.s3.amazonaws.com/index.html)


