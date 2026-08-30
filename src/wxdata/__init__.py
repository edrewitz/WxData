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

"""
********************************************************************************


************  This section hosts the Model Data Clients. ***********************


********************************************************************************
"""

##############
#### NOAA ####
##############
# Global Forecast System (GFS)
# - GFS 0.25x0.25 Degree Primary Parameters
# - GFS 0.25x0.25 Degree Secondary Parameters
# - GFS 0.5x0.5 Degree
from wxdata.model_data.noaa.gfs.gfs import(
    gfs_0p25,
    gfs_0p25_secondary_parameters,
    gfs_0p50
)

# AI Global Forecast System (AIGFS)
from wxdata.model_data.noaa.aigfs.aigfs import aigfs

# Hybrid Global Ensemble Forecast System (HGEFS)
from wxdata.model_data.noaa.hgefs.hgefs import hgefs_mean_spread

# Global Ensemble Forecast System (GEFS)
# - GEFS 0.5x0.5 Degree Primary Parameters
# - GEFS 0.5x0.5 Degree Secondary Parameters
# - GEFS 0.25x0.25 Degree
from wxdata.model_data.noaa.gefs.gefs import(
    gefs_0p50,
    gefs_0p50_secondary_parameters,
    gefs_0p25
)

# Climate Forecast System (CFS)
# - CFS Flux Products
# - CFS Pressure Products
from wxdata.model_data.noaa.cfs.cfs import(
    cfs_flux,
    cfs_pressure
)

# AI Global Ensemble Forecast System (AIGEFS)
# - AIGEFS Pressure Members (Pressure Level Variables)
# - AIGEFS Surface Members (Surface Level Variables)
# - AIGEFS Single (AIGEFS Ensemble Mean & AIGEFS Ensemble Spread)
from wxdata.model_data.noaa.aigefs.aigefs import(
    aigefs_pressure_members,
    aigefs_surface_members,
    aigefs_single
)

# Real-Time Mesoscale Analysis (RTMA)
# - RTMA Latest 
# - RTMA Comparison Between Two Times 
from wxdata.model_data.noaa.rtma.rtma import(
    rtma, 
    rtma_comparison
)

##############################################################
# European Centre for Medium-Range Weather Forecasts (ECMWF) #
##############################################################
# - ECMWF IFS
# - ECMWF IFS Ensemble
# - ECMWF AIFS
# - ECMWF AIFS Ensemble
# - ECMWF IFS Wave
# - ECMWF IFS Wave Ensemble
from wxdata.model_data.ecmwf.ecmwf import(
    ecmwf_ifs,
    ecmwf_ifs_ens,
    ecmwf_aifs,
    ecmwf_aifs_ens,
    ecmwf_ifs_wave,
    ecmwf_ifs_wave_ens
)

##################################
# Canadian Meteorological Center #
##################################
# - Canadian Global Deterministic Prediction System (GDPS)
# - Canadian Regional Deterministic Prediction System (RDPS)
# - Canadian High Resolution Deterministic Prediction System (HRDPS)
# - Canadian Global Ensemble Prediction System (GEPS)
# - Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Forecasts
# - Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Hindcasts
from wxdata.model_data.cmc.gdps.gdps import gdps
from wxdata.model_data.cmc.rdps.rdps import rdps
from wxdata.model_data.cmc.hrdps.hrdps import hrdps
from wxdata.model_data.cmc.geps.geps import geps
from wxdata.model_data.cmc.cansips.forecast.cansips_forecast import cansips_forecast
from wxdata.model_data.cmc.cansips.hindcast.cansips_hindcast import cansips_hindcast



"""
********************************************************************************


************  This section hosts the Fuels Data Clients.  **********************


********************************************************************************
"""

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
from wxdata.fuels_data.fems.observations import(
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
from wxdata.fuels_data.fems.meta_data import(
    get_single_raws_station_meta_data,
    get_multi_raws_station_meta_data
)


"""
********************************************************************************


************  This section hosts the Gridded Forecast Data Clients.  ***********


********************************************************************************
"""

# NOAA 
# - Storm Prediction Center Outlooks
# - Climate Prediction Center Outlooks
# - National Weather Service Forecasts
from wxdata.gridded_forecasts.noaa.nws.nws import(
    get_ndfd_grids,
    get_cpc_outlook
)

"""
*****************************************************************************


************  This section hosts the Observational Data Clients. ************


*****************************************************************************
"""

# Observed Upper-Air Soundings
# (University of Wyoming Database)
from wxdata.observational_data.soundings.wyoming_soundings import get_observed_sounding_data

# METAR Observational Data (From NOAA)
from wxdata.observational_data.metars.metar_obs import download_metar_data

# NEXRAD2 Radar Data
# - NEXRAD2 Radar Single Station
# - NEXRAD2 Radar Multi Station
from wxdata.observational_data.radar.nexrad2 import(
    download_current_single_station_nexrad2_radar_data,
    download_current_multi_station_nexrad2_radar_data
)

"""
*********************************************************************************


************  This section hosts the Model Data Processors. *********************


*********************************************************************************
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

# Canadian Meteorological Center Gridded Models
# - Canadian Global Deterministic Prediction System (GDPS)
# - Canadian Regional Deterministic Prediction System (RDPS)
# - Canadian High Resolution Deterministic Prediction System (HRDPS)
# - Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Forecast
# - Canadian Seasonal to Inter-annual Prediction System (CanSIPS) Hindcast
import wxdata.post_processors.cmc_post_processing as cmc_post_processing

# Real-Time Mesoscale Analysis (RTMA)
from wxdata.post_processors.rtma_post_processing import process_rtma_data


"""
****************************************************************************************************************


************  This section hosts the Data Querying/Transforming Tools & Automation Tools. **********************


****************************************************************************************************************
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
***************************************************************************


************  This section hosts the Raw Data Clients. ********************


***************************************************************************
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
***********************************************************************************


************  This section hosts the API Interface Clients. ***********************


***********************************************************************************
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
import wxdata.api.open_meteo_api.weather_forecasts.noaa as open_meteo_api_noaa
import wxdata.api.open_meteo_api.weather_forecasts.ecmwf as open_meteo_api_ecmwf
import wxdata.api.open_meteo_api.weather_forecasts.dwd as open_meteo_api_dwd
import wxdata.api.open_meteo_api.weather_forecasts.meteo_france as open_meteo_api_meteo_france
import wxdata.api.open_meteo_api.weather_forecasts.cmc as open_meteo_api_cmc
import wxdata.api.open_meteo_api.weather_forecasts.jma as open_meteo_api_jma
import wxdata.api.open_meteo_api.weather_forecasts.ukmo as open_meteo_api_ukmo
import wxdata.api.open_meteo_api.weather_forecasts.current_weather as open_meteo_api_current_weather
import wxdata.api.open_meteo_api.weather_forecasts.google as open_meteo_api_google

### Seasonal Forecasts (ECMWF EC46 & SEAS5) ###

# - Daily Data (EC46 & SEAS5)
# - Weekly Data (EC46)
# - Monthly Data (SEAS5)
import wxdata.api.open_meteo_api.seasonal_forecasts.ecmwf_daily as open_meteo_api_ecmwf_seasonal_forecasts_daily
import wxdata.api.open_meteo_api.seasonal_forecasts.ecmwf_weekly as open_meteo_api_ecmwf_seasonal_forecasts_weekly
import wxdata.api.open_meteo_api.seasonal_forecasts.ecmwf_monthly as open_meteo_api_ecmwf_seasonal_forecasts_monthly

### Climate Data ###
import wxdata.api.open_meteo_api.climate.climate_data as open_meteo_api_climate_data

### Air Quality Information ###
import wxdata.api.open_meteo_api.air_quality.cams as open_meteo_api_air_quality

### Marine Forecasts ###
# - Meteo-France
# - Deutscher Wetterdienst (DWD)
# - ECMWF
# - NOAA
import wxdata.api.open_meteo_api.marine_forecasts.meteo_france as open_meteo_api_meteo_france_marine
import wxdata.api.open_meteo_api.marine_forecasts.dwd as open_meteo_api_dwd_marine
import wxdata.api.open_meteo_api.marine_forecasts.ecmwf as open_meteo_api_ecmwf_marine
import wxdata.api.open_meteo_api.marine_forecasts.noaa as open_meteo_api_noaa_marine

### Solar Radiation Forecasts ### 
import wxdata.api.open_meteo_api.solar_radiation.solar_radiation as open_meteo_api_solar_radiation

###################
### Air-Now API ###
###################

# Air-Now API: https://docs.airnowapi.org/

# - Observations
import wxdata.api.airnow_api.observations as air_now_observations