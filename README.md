<img src="https://github.com/edrewitz/WxData/blob/main/icons/weather%20icon.jpg?raw=true" width="200" alt="Alt text" /> <img src="https://github.com/edrewitz/WxData/blob/1be590e9a16033974a592d8cf99f3cd521f95e0b/icons/python%20logo.png?raw=true" width="200" alt="Alt text" />

[![Conda Recipe](https://img.shields.io/badge/recipe-wxdata-green.svg)](https://anaconda.org/conda-forge/wxdata) [![Conda Version](https://img.shields.io/conda/vn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata) ![PyPI](https://img.shields.io/pypi/v/wxdata?label=pypi%20wxdata) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/license.svg)](https://anaconda.org/conda-forge/wxdata) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/wxdata/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/wxdata) 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17727621.svg)](https://doi.org/10.5281/zenodo.17727621)



Anaconda Downloads

[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/wxdata.svg)](https://anaconda.org/conda-forge/wxdata)


PIP Downloads:

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/wxdata?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wxdata)



**(C) Eric J. Drewitz 2025-2026**

A Python package consisting of the following:

1) End-to-end weather data clients with VPN/PROXY support
2) Raw data clients with VPN/PROXY support
3) Data processors that decode variable keys from GRIB format into a plain-language format
4) Various tools for assisting Python automated workflows, querying meteorological datasets and filling gaps in meteorological data.
5) Has interfaces with various weather APIs. 

# Table of Contents

1) [Installation Instructions](https://edrewitz.github.io/WxData/#installation-instructions)

2) [Server List (For End-To-End Clients That Can Rotate Between Servers)](https://edrewitz.github.io/WxData/#server-list)

3) [Proxy Server Configuration](https://edrewitz.github.io/WxData/#proxy-server-configuration)

4) [What makes WxData unique among various meteorological Python packages?](https://edrewitz.github.io/WxData/#what-makes-wxdata-unique-among-various-meteorological-python-packages)

5) [WxData Tutorials](https://edrewitz.github.io/WxData/#wxdata-tutorials)

6) [WxData Documentation](https://edrewitz.github.io/WxData/#wxdata-documentation)

7) [Importing Functions from WxData](https://edrewitz.github.io/WxData/#importing-functions-from-wxdata)

8) [Citations](https://edrewitz.github.io/WxData/#citations)

9) [Data Sources]()


## Installation Instructions

**How To Install**

Copy and paste either command into your terminal or anaconda prompt:

*Install via Anaconda*

`conda install wxdata`

OR

`mamba install wxdata`

*Install via pip*

`pip install wxdata`

**How To Update To The Latest Version**

Copy and paste either command into your terminal or anaconda prompt:

*Update via Anaconda*

***This is for users who initially installed WxData through Anaconda***

`conda update wxdata`

OR

`mamba update wxdata`

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
## Server List



<img src="https://github.com/edrewitz/WxData/blob/main/icons/noaa_rotation.png?raw=true" width="200" alt="Alt text" /> <img src="https://github.com/edrewitz/WxData/blob/main/icons/ecmwf_rotation.png?raw=true" width="200" alt="Alt text" />

End-To-End clients with multiple servers to pull data from can find the different options for `source` by the table below

`source='noaa' - NOAA/NCEP/NOMADS OR NOAA/NWS/FTP`

`source='ecmwf' - ECMWF Open-Data Server`

`source='aws' - Amazon Web Services (AWS)`

`source='google' - Google Cloud`


| Client | NOAA/NCEP/NOMADS | ECMWF Open-Data | Amazon AWS | Google Cloud | NOAA/NWS/FTP |
| -------- | -------- | -------- | -------- | -------- | -------- |
| GFS0P25  |Y|N|Y|Y|N|
| GFS0P25 SECONDARY PARAMETERS  |Y|N|Y|Y|N| 
| GFS0P50  |Y|N|Y|Y|N|
| GEFS0P50  |Y|N|Y|Y|N|
| GEFS0P50 SECONDARY PARAMETERS  |Y|N|Y|Y|N|
| GEFS0P25  |Y|N|Y|Y|N|
| ECMWF IFS |N|Y|Y|Y|N|
| ECMWF IFS Ensemble |N|Y|Y|Y|N|
| ECMWF AIFS|N|Y|Y|Y|N|
| ECMWF AIFS Ensemble|N|Y|Y|Y|N|
| ECMWF IFS Wave |N|Y|Y|Y|N|
| ECMWF IFS Wave Ensemble |N|Y|Y|Y|N|
| Get NDFD Grids |N|N|Y|N|Y|
| RTMA |Y|N|Y|N|N|

---------------------------------------------------------

## Proxy Server Configuration

***Friendly for users working on VPN/PROXY connections***

   Depending on which client, the proxy-address:port must be entered as either a dictionary or a string.

   The clients that use a string for proxies are:

   1) All ECMWF clients.

   2) METAR Observations Client.
      
   3) `pixel_query()` tool if the user needs to download the airport station codes list.

   All other clients use proxies as a dictionary

Example: We want to download the latest Observed Sounding Data for San Diego, CA (NKX)

```python
proxies=None ---> proxies={
                       'http':'http://your-proxy-address:port',
                       'https':'http://your-proxy-address:port'
                       }
```
```python
# Here is our program
from wxdata import get_observed_sounding_data

proxies={
        'http':'http://your-proxy-address:port',
        'https':'http://your-proxy-address:port'
        }

data = sounding_data = get_observed_sounding_data('nkx', proxies=proxies)
```

Example: We want to download the ECMWF IFS Data:

```python
proxies=None ---> proxies="http://your-proxy-address:port" ---> ds = ecmwf_ifs(proxies=proxies)
```
```python
# Here is our program
from wxdata import get_observed_sounding_data

proxies="https://your-proxy-address:port"

data = ecmwf_ifs(proxies=proxies)
```

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

7) Utilizes byte-range requests to subset and speed up download times.

8) Several end-to-end clients have the ability to pull from multiple servers (NOAA/NCEP/NOMADS, ECMWF Open-Data, Amazon Web Services (AWS), Google Cloud and NOAA/NWS/FTP).

9) Clients can automatically rotate to a new server when experiencing connectivity issues to the initial server. 

-----------------------------------------------
    
## WxData Tutorials

### Regular Users
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

20) [Downloading NEXRAD II Radar Data and then plotting it in Py-ART](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/NEXRADII.ipynb)

21) [Downloading 30 Days of 6hrly CFS Data and plotting the 30-Day time-mean for mean sea level pressure across the Northern Hemisphere](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/cfs.ipynb)

22) [Download all 50 Ensemble Members of the ECMWF IFS Ensemble for 2-Meter Temperature Using the Open-Meteo API and Make an Ensemble Spaghetti Plot](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/ecmwf_ifs_ens_spaghetti.ipynb)

23) [Download Solar Radiation Forecasts Using Open-Meteo API](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/open_meteo_api_solar_radiation.ipynb)

24) [Download Latest Fine Particulates PM2.5 and Ozone (O3) Observations Using Air Now API](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/air_now_api.ipynb)

### Advanced Users

1) [Using the `client` module to download the latest HadCRUT5 Analysis netCDF file and open this dataset in xarray](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/hadcrut5.ipynb)

2) [Downloading the GFS0P25 for temperature fields and using run_external_scripts() to post-process this GFS0P25 dataset in an external Python script](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/external_scripts.ipynb)

3) [Downloading GFS Data Using Byte-Range Requests](https://github.com/edrewitz/WxData-JupyterLab-Examples/blob/main/bytes_range_request.ipynb)

---------------------------------------------------

## WxData Documentation

### Documentation Sections

1. [End-To-End Data Clients](https://github.com/edrewitz/WxData?tab=readme-ov-file#end-to-end-data-clients)
2. [Raw Data Clients](https://github.com/edrewitz/WxData?tab=readme-ov-file#raw-data-clients)
3. [Post-Processors](https://github.com/edrewitz/WxData?tab=readme-ov-file#post-processors)
4. [Data Querying Tools](https://github.com/edrewitz/WxData?tab=readme-ov-file#data-querying-tools)
5. [Data Transformation & Gap Filling Tools](https://github.com/edrewitz/WxData?tab=readme-ov-file#data-transformation--gap-filling-tools)
6. [Automated Python Workflow Tools](https://github.com/edrewitz/WxData?tab=readme-ov-file#automated-python-workflow-tools)
7. [Open-Meteo API](https://github.com/edrewitz/WxData/blob/main/README.md#open-meteo-api)

#### End-To-End Data Clients

##### ***Global Forecast System (GFS)***
1. [GFS0P25](https://edrewitz.github.io/WxData/GFS0P25)
2. [GFS0P25 SECONDARY PARAMETERS](https://edrewitz.github.io/WxData/GFS0P25%20Secondary%20Parameters)
3. [GFS0P50](https://edrewitz.github.io/WxData/GFS0P50)

##### ***AI Global Forecast System (AIGFS)***
1. [AIGFS](https://edrewitz.github.io/WxData/aigfs)

##### ***Climate Forecast System (CFS)***
1. [CFS Pressure](https://edrewitz.github.io/WxData/cfs_pressure)
2. [CFS Flux](https://edrewitz.github.io/WxData/cfs_flux)

##### ***Hybrid Global Ensemble Forecast System (HGEFS)***
1. [HGEFS](https://edrewitz.github.io/WxData/hgefs)

##### ***Global Ensemble Forecast System (GEFS)***
1. [GEFS0P50](https://edrewitz.github.io/WxData/GEFS0P50)
2. [GEFS0P50 SECONDARY PARAMETERS](https://edrewitz.github.io/WxData/GEFS0P50%20Secondary%20Parameters)
3. [GEFS0P25](https://edrewitz.github.io/WxData/GEFS0P25)

##### ***AI Global Ensemble Forecast System (AIGEFS)***
1. [AIGEFS Members (Pressure Parameters)](https://edrewitz.github.io/WxData/aigefs_pressure_members)
2. [AIGEFS Members (Surface Parameters)](https://edrewitz.github.io/WxData/aigefs_surface_members)
3. [AIGEFS Ensemble Mean & Ensemble Spread](https://edrewitz.github.io/WxData/aigefs_single)

##### ***ECMWF Open Data***
1. [ECMWF IFS](https://edrewitz.github.io/WxData/ECMWF_IFS)
2. [ECMWF IFS Ensemble](https://edrewitz.github.io/WxData/ECMWF%20IFS%20Ensemble)
3. [ECMWF AIFS](https://edrewitz.github.io/WxData/ECMWF_AIFS)
4. [ECMWF AIFS Ensemble](https://edrewitz.github.io/WxData/ECMWF%20AIFS%20Ensemble)
5. [ECMWF IFS Wave](https://edrewitz.github.io/WxData/ECMWF_IFS_Wave)
6. [ECMWF IFS Wave Ensemble](https://edrewitz.github.io/WxData/ECMWF%20IFS%20Wave%20Ensemble)
   
##### ***Real-Time Mesoscale Analysis (RTMA)***
1. [RTMA](https://edrewitz.github.io/WxData/rtma)
2. [RTMA Comparison](https://edrewitz.github.io/WxData/rtma%20comparison)

##### ***NOAA Storm Prediction Center Outlooks/Climate Prediction Center Outlooks/National Weather Service Forecasts***
1. [Get NDFD Grids](https://edrewitz.github.io/WxData/noaa)
2. [Climate Prediction Center Outlooks](https://edrewitz.github.io/WxData/cpc_outlooks)

##### ***METAR Observations***
1. [METAR Observations](https://edrewitz.github.io/WxData/metars)

##### ***FEMS RAWS Network***
1. [Get Single Station Weather Observations](https://edrewitz.github.io/WxData/single%20raws%20weather%20obs)
2. [Get Single Station Fuels Observations](https://edrewitz.github.io/WxData/single%20raws%20fuels%20obs)
3. [Get Multi Station Weather Observations](https://edrewitz.github.io/WxData/multi%20raws%20weather%20obs)
4. [Get Multi Station Fuels Observations](https://edrewitz.github.io/WxData/multi%20raws%20fuels%20obs)
5. [Get Current Multi Station Weather Observations](https://edrewitz.github.io/WxData/current%20multi%20raws%20weather%20obs)
6. [Get Current Multi Station Fuels Observations](https://edrewitz.github.io/WxData/current%20multi%20raws%20fuels%20obs)
7. [Get Current Multi Station Weather Observations By State](https://edrewitz.github.io/WxData/raws%20weather%20obs%20by%20state)
8. [Get Current Multi Station Fuels Observations By State](https://edrewitz.github.io/WxData/raws%20fuels%20obs%20by%20state)
9. [Get Single Station Weather Forecast](https://edrewitz.github.io/WxData/single%20raws%20weather%20forecast)
10. [Get Single Station NFDRS (Fuels) Forecast](https://edrewitz.github.io/WxData/single%20raws%20nfdrs%20forecast)
11. [Get Multi Station Weather Forecast](https://edrewitz.github.io/WxData/multi%20raws%20weather%20forecast)
12. [Get Multi Station NFDRS (Fuels) Forecast](https://edrewitz.github.io/WxData/multi%20raws%20nfdrs%20forecast)
13. [Get Single Station Meta-Data](https://edrewitz.github.io/WxData/raws%20single%20station%20meta%20data)
14. [Get Multi Station Meta-Data](https://edrewitz.github.io/WxData/raws%20multi%20station%20meta%20data)

##### ***Observed Atmospheric Soundings***
1. [University Of Wyoming Soundings](https://edrewitz.github.io/WxData/wyoming_soundings)

##### ***NEXRAD II Radar Data***
1. [Single Site](https://edrewitz.github.io/WxData/nexrad2_single)
2. [Multi-Site](https://edrewitz.github.io/WxData/nexrad2_multi)

-----------------------------

#### Post-Processors

##### ***GFS Post-Processing***
1. [Primary GFS Post-Processing](https://edrewitz.github.io/WxData/Primary%20GFS%20Post%20Processing)
2. [Secondary GFS Post-Processing](https://edrewitz.github.io/WxData/Secondary%20GFS%20Post%20Processing)

##### ***AIGFS Post-Processing***
1. [AIGFS Post-Processing](https://edrewitz.github.io/WxData/aigfs_post_processing)

##### ***CFS Post-Processing***
1. [CFS Pressure Post-Processing](https://edrewitz.github.io/WxData/cfs_pressure_post_processing)
2. [CFS Flux Post-Processing](https://edrewitz.github.io/WxData/cfs_flux_post_processing)

##### ***GEFS Post-Processing***
1. [Primary GEFS Post-Processing](https://edrewitz.github.io/WxData/Primary%20GEFS%20Post-Processing)
2. [Secondary GEFS Post-Processing](https://edrewitz.github.io/WxData/Secondary%20GEFS%20Post%20Processing)

##### ***AIGEFS Post-Processing***
1. [AIGEFS Members Post-Processing](https://edrewitz.github.io/WxData/aigefs_members_post_processing)
2. [AIGEFS Single Post-Processing](https://edrewitz.github.io/WxData/aigefs_single_post_processing)

##### ***HGEFS Post-Processing***
1. [HGEFS Post-Processing](https://edrewitz.github.io/WxData/hgefs_post_processing)

##### ***ECMWF Post-Processing***
1. [ECMWF IFS and IFS Ensemble](https://edrewitz.github.io/WxData/ECMWF%20IFS%20Post%20Processing)
2. [ECMWF AIFS and AIFS Ensemble](https://edrewitz.github.io/WxData/ECMWF%20AIFS%20Post%20Processing)
3. [ECMWF IFS Wave and IFS Wave Ensemble](https://edrewitz.github.io/WxData/ECMWF%20IFS%20Wave%20Post%20Processing)

##### ***Real-Time Mesoscale Analysis Post-Processing***
1. [RTMA](https://edrewitz.github.io/WxData/RTMA%20Post%20Processing)

-----------------------------------------------

#### Raw Data Clients

##### ***xmACIS2 Climate Data***
1. [xmACIS2 Client](https://edrewitz.github.io/WxData/xmacis2_client)

##### ***Custom Gridded Data***
1. [Gridded Data Client](https://edrewitz.github.io/WxData/get_gridded_data)

##### ***Custom CSV Data***
1. [CSV Data Client](https://edrewitz.github.io/WxData/get_csv_data)

##### ***Custom Excel Data***
1. [Excel Data Client](https://edrewitz.github.io/WxData/get_excel_data)

##### ***AWS Open Data***
1. [AWS Open Data](https://edrewitz.github.io/WxData/get_open_aws_data)

##### ***Byte-Range Requests***
1. [Byte-Range Requests](https://edrewitz.github.io/WxData/bytes_range_request)

---------------------------------------------------------------

#### Data Querying Tools

##### ***Pixel Query***
1. [pixel_query](https://edrewitz.github.io/WxData/pixel_query)

##### ***Line Query***
1. [line_query](https://edrewitz.github.io/WxData/line_query)

--------------------------------------------------

#### Data Transformation & Gap Filling Tools

##### ***Cyclic Points For Hemispheric Plots***
1. [Cyclic Points](https://edrewitz.github.io/WxData/cyclic_point)

##### ***Shifting Longitude From 0 to 360 --> -180 to 180***
1. [shift_longitude](https://edrewitz.github.io/WxData/shift_longitude)

##### ***Linear Anti-Aliasing Between Two Points***
1. [linear_anti_aliasing](https://edrewitz.github.io/WxData/linear_anti_aliasing)

------------------------------------------

#### Automated Python Workflow Tools

##### ***Running External Python Scripts In Your Workflow***

1 [run_external_scripts](https://edrewitz.github.io/WxData/run_external_scripts)

---------------------------------------

#### Open-Meteo API

##### Weather Forecasts 
###### ***Current Weather***
1. [Current Weather](https://edrewitz.github.io/WxData/open%20meteo%20api%20current%20weather)

###### ***National Oceanic and Atmospheric Administrationn (NOAA)***
1. [GFS](https://edrewitz.github.io/WxData/open%20meteo%20api%20noaa%20gfs)
2. [GEFS](https://edrewitz.github.io/WxData/open%20meteo%20api%20noaa%20gefs)
3. [AIGFS](https://edrewitz.github.io/WxData/open%20meteo%20api%20noaa%20aigfs)
4. [AIGEFS](https://edrewitz.github.io/WxData/open%20meteo%20api%20noaa%20aigefs)
5. [HGEFS](https://edrewitz.github.io/WxData/open%20meteo%20api%20noaa%20hgefs)
6. [NBM](https://edrewitz.github.io/WxData/open%20meteo%20api%20noaa%20nbm)

###### ***European Centre for Medium-Range Weather Forecasts (ECMWF)***
1. [IFS](https://edrewitz.github.io/WxData/open%20meteo%20api%20ecmwf%20ifs)
2. [AIFS](https://edrewitz.github.io/WxData/open%20meteo%20api%20ecmwf%20aifs)
3. [IFS HRES](https://edrewitz.github.io/WxData/open%20meteo%20api%20ecmwf%20ifs%20hres)
4. [IFS Ensemble](https://edrewitz.github.io/WxData/open%20meteo%20api%20ecmwf%20ifs%20ens)
5. [AIFS Ensemble](https://edrewitz.github.io/WxData/open%20meteo%20api%20ecmwf%20aifs%20ens)

###### ***Canadian Meteorological Centre (CMC)***
1. [GEM](https://edrewitz.github.io/WxData/open%20meteo%20api%20cmc%20gem)
2. [GEM Ensemble](https://edrewitz.github.io/WxData/open%20meteo%20api%20cmc%20gem%20ens)

###### ***Deutscher Wetterdienst (DWD)***
1. [ICON](https://edrewitz.github.io/WxData/open%20meteo%20api%20dwd%20icon)
2. [ICON EPS](https://edrewitz.github.io/WxData/open%20meteo%20api%20dwd%20icon%20eps)

###### ***Meteo-France***
1. [ARPEGE](https://edrewitz.github.io/WxData/open%20meteo%20api%20meteo%20france%20arpege)

###### ***Japan Meteorological Agency (JMA)***
1. [JMA](https://edrewitz.github.io/WxData/open%20meteo%20api%20jma%20jma)

###### ***UK Met Office (UKMO)***
1. [UKMO Global Ensemble](https://edrewitz.github.io/WxData/open%20meteo%20api%20ukmo%20global%20ens)

###### ***Google***
1. [Weather Next 2 All Ensemble Members](https://edrewitz.github.io/WxData/open%20meteo%20api%20google%20weather%20next%202%20members)
2. [Weather Next 2 Ensemble Mean](https://edrewitz.github.io/WxData/open%20meteo%20api%20google%20weather%20next%202%20ensemble%20mean)

##### Marine Forecasts

###### ***National Oceanic and Atmospheric Administrationn (NOAA)***
1. [GFS0P25 Wave Forecasts](https://edrewitz.github.io/WxData/open%20meteo%20api%20gfs0p25%20wave)
2. [GFS0P16 Wave Forecasts](https://edrewitz.github.io/WxData/open%20meteo%20api%20gfs0p16%20wave)

###### ***European Centre for Medium-Range Weather Forecasts (ECMWF)***
1. [ECMWF Wave Model](https://edrewitz.github.io/WxData/open%20meteo%20api%20ecmwf%20wam)
2. [ECMWF Wave Model 0.25 Degree](https://edrewitz.github.io/WxData/open%20meteo%20api%20ecmwf%20wam%200p25)

###### ***Meteo-France***
1. [Meteo-France Wave Model](https://edrewitz.github.io/WxData/open%20meteo%20api%20meteo%20france%20wave)
2. [Meteo-France Ocean Currents Model](https://edrewitz.github.io/WxData/open%20meteo%20api%20meteo%20france%20ocean%20currents)

###### ***Deutscher Wetterdienst (DWD)***
1. [European Domain Wave Model](https://edrewitz.github.io/WxData/open%20meteo%20api%20ewam)
2. [Global Domian Wave Model](https://edrewitz.github.io/WxData/open%20meteo%20api%20gwam)

##### Seasonal Forecasts

###### ***Daily Forecasts***
1. [ECMWF EC46 + SEAS5 Ensemble Members](https://edrewitz.github.io/WxData/open%20meteo%20api%20ec46%20seas5%20daily)
2. [ECMWF EC46 Ensemble Members](https://edrewitz.github.io/WxData/open%20meteo%20api%20ec46%20daily)
3. [ECMWF SEAS5 Ensemble Members](https://edrewitz.github.io/WxData/open%20meteo%20api%20seas5%20daily)
4. [ECMWF EC46 + SEAS5 Ensemble Mean](https://edrewitz.github.io/WxData/open%20meteo%20api%20ec46%20seas5%20daily%20ensemble%20mean)
5. [ECMWF EC46 Ensemble Mean](https://edrewitz.github.io/WxData/open%20meteo%20api%20ec46%20daily%20ensemble%20mean)
6. [ECMWF SEAS5 Ensemble Mean](https://edrewitz.github.io/WxData/open%20meteo%20api%20seas5%20daily%20ensemble%20mean)

###### ***Weekly Forecasts***
1. [ECMWF EC46 Mean & Anomaly](https://edrewitz.github.io/WxData/open%20meteo%20api%20ec46%20weekly%20mean%20anomaly)

###### ***Monthly Forecasts***
1. [ECMWF SEAS5 Mean & Anomaly](https://edrewitz.github.io/WxData/open%20meteo%20api%20seas5%20monthly%20mean%20anomaly)

##### Climate Reanalysis & Forecasts
1. [CMCC-CM2-VHR4](https://edrewitz.github.io/WxData/open%20meteo%20api%20cmcc_cm2_vhr4%20forecasts)
2. [FGOALS_f3_H](https://edrewitz.github.io/WxData/open%20meteo%20api%20fgoals_f3_h%20forecasts)
3. [HiRAM_SIT_HR](https://edrewitz.github.io/WxData/open%20meteo%20api%20hiram_sit_hr%20forecasts)
4. [MRI_AGCM3_2_S](https://edrewitz.github.io/WxData/open%20meteo%20api%20mri_agcm3_2_s%20forecasts)
5. [EC_Earth3P_HR](https://edrewitz.github.io/WxData/open%20meteo%20api%20ec_earth3p_hr%20forecasts)
6. [MPI_ESM1_2_XR](https://edrewitz.github.io/WxData/open%20meteo%20api%20mpi_esm1_2_xr%20forecasts)
7. [NICAM16_8S](https://edrewitz.github.io/WxData/open%20meteo%20api%20nicam16_8s%20forecasts)

##### Air Quality Forecasts
1. [CAMS](https://edrewitz.github.io/WxData/open%20meteo%20api%20air%20quality)

##### Solar Radiation Forecasts
1. [Solar Radiation Forecast](https://edrewitz.github.io/WxData/open%20meteo%20api%20solar%20radiation)

---------------------------------------

#### Air Now API

##### ***Observations***
1. [Get Current Data Bounding Box](https://edrewitz.github.io/WxData/air%20now%20api%20observations)
2. [Get Historical Data Bounding Box](https://edrewitz.github.io/WxData/air%20now%20api%20historical%20observations)

---------------------------------------

## Importing Functions from WxData

```Python
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
#  - get_aws_open_data()
#  - byte_range_request()
import wxdata.client.client as client

"""
***************************************************************************


************  This section hosts the different API Interfaces.  ***********


***************************************************************************
"""
#######################
### Open-Meteo API ###
#######################

# Open-Meteo API: https://open-meteo.com/

### Weather Forecasts ###

# - NOAA/NCEP Models
# - ECMWF Models
# - Deutscher Wetterdienst (DWD) Models
# - Meteo-France Models
# - CMC Models
# - Japan Meteorological Agency (JMA) Models
# - UK Met Office (UKMO)
# - Current Weather (Model Mosaic)
# - Google (Weather Next 2 Ensemble)
import wxdata.open_meteo_api.weather_forecasts.noaa as open_meteo_api_noaa
import wxdata.open_meteo_api.weather_forecasts.ecmwf as open_meteo_api_ecmwf
import wxdata.open_meteo_api.weather_forecasts.dwd as open_meteo_api_dwd
import wxdata.open_meteo_api.weather_forecasts.meteo_france as open_meteo_api_meteo_france
import wxdata.open_meteo_api.weather_forecasts.cmc as open_meteo_api_cmc
import wxdata.open_meteo_api.weather_forecasts.jma as open_meteo_api_jma
import wxdata.open_meteo_api.weather_forecasts.ukmo as open_meteo_api_ukmo
import wxdata.open_meteo_api.weather_forecasts.current_weather as open_meteo_api_current_weather
import wxdata.open_meteo_api.weather_forecasts.google as open_meteo_api_google

### Seasonal Forecasts (ECMWF EC46 & SEAS5) ###

# - Daily Data (EC46 & SEAS5)
# - Weekly Data (EC46)
# - Monthly Data (SEAS5)
import wxdata.open_meteo_api.seasonal_forecasts.ecmwf_daily as open_meteo_api_ecmwf_seasonal_forecasts_daily
import wxdata.open_meteo_api.seasonal_forecasts.ecmwf_weekly as open_meteo_api_ecmwf_seasonal_forecasts_weekly
import wxdata.open_meteo_api.seasonal_forecasts.ecmwf_monthly as open_meteo_api_ecmwf_seasonal_forecasts_monthly

### Climate Data ###
import wxdata.open_meteo_api.climate.climate_data as open_meteo_api_climate_data

### Air Quality Information ###
import wxdata.open_meteo_api.air_quality.cams as open_meteo_api_air_quality

### Marine Forecasts ###
# - Meteo-France
# - Deutscher Wetterdienst (DWD)
# - ECMWF
# - NOAA
import wxdata.open_meteo_api.marine_forecasts.meteo_france as open_meteo_api_meteo_france_marine
import wxdata.open_meteo_api.marine_forecasts.dwd as open_meteo_api_dwd_marine
import wxdata.open_meteo_api.marine_forecasts.ecmwf as open_meteo_api_ecmwf_marine
import wxdata.open_meteo_api.marine_forecasts.noaa as open_meteo_api_noaa_marine

### Solar Radiation Forecasts ### 
import wxdata.open_meteo_api.solar_radiation.solar_radiation as open_meteo_api_solar_radiation

###################
### Air-Now API ###
###################

# Air-Now API: https://docs.airnowapi.org/

# - Observations
import wxdata.airnow_api.observations as air_now_observations

```
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

10) [Open-Meteo API](https://open-meteo.com/)

11) [Air Now API](https://docs.airnowapi.org/webservices)



