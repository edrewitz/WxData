"""
This file hosts the WxData Command Line Interface for retrieving European Centre for Medium-Range Weather Forecasts (ECMWF) Data.

Command Line Use: `wxdata-ecmwf **args`

(C) Eric J. Drewitz 2025-2026
"""

import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.ecmwf.ecmwf import(
    ecmwf_ifs as _fetch_ecmwf_ifs,
    ecmwf_ifs_ens as _fetch_ecmwf_ifs_ens,
    ecmwf_aifs as _fetch_ecmwf_aifs,
    ecmwf_aifs_ens as _fetch_ecmwf_aifs_ens,
    ecmwf_ifs_wave as _fetch_ecmwf_ifs_wave,
    ecmwf_ifs_wave_ens as _fetch_ecmwf_ifs_wave_ens
)


def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-gfs -h to view the help documentation.")
    print(f"Please visit: https://github.com/edrewitz/WxData/wiki#ecmwf-open-data for full detailed documentation.")
    
# ---------------------------------------------------------------------
# Top-level CLI group
# ---------------------------------------------------------------------
@_click.group(context_settings={"help_option_names": ["-h", "--help"]})
def ecmwf_data():
    """GFS command line utilities."""
    pass

# ---------------------------------------------------------------------
# ECMWF Commands
# ---------------------------------------------------------------------
@ecmwf_data.group(name='ifs')
def ifs():
    
    """
    **Downloads The Latest ECMWF IFS Data**
    
    ***Valid Commands***
    
    -f = Final Forecast Hour (Default=360).
     
    00z & 12z Runs Have 360 hours
    
    06z & 18z Runs Have 144 hours
    
    -s = Source (Default=ecmwf). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices***
    
    ecmwf - ECMWF Open-Data
    
    aws - Amazon Web Services
    
    google - Google Cloud Servers
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:ECMWF/IFS. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variables(Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 
                       
    The list of variables the user wants to query.
    
    Here is a sample of how to query geopotential height and temperature at 500mb `wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 500`
    
    ***Variable List***
    
    'Geopotential (step 0)'
    
    'Standard deviation of sub-gridscale orography (step 0)'
    
    '10-meter u-wind component'
    
    '10-meter v-wind component'
    
    '100-meter u-wind component'
    
    '100-meter v-wind component'
    
    'maximum 10-meter wind gust step 0'
    
    'maximum 10-meter wind gust steps 3-144'
    
    '2-meter temperature'
    
    '2-meter dewpoint temperature'
    
    'mean sea level pressure'
    
    'mean zero-crossing wave period'
    
    'mean wave direction'
    
    'mean wave period'
    
    'peak wave period'
    
    'significant wave height'
    
    'runoff'
    
    'total precipitation'
    
    'surface pressure'
    
    'total column vertically integrated water vapor'
    
    'total cloud cover'
    
    'snow depth water equivalent'
    
    'snowfall water equivalent'
    
    'land sea mask'
    
    'volumetric soil moisture content'
    
    'soil temperature'
    
    'most unstable cape'
    
    'snow albedo'
    
    '3-hour minimum 2-meter temperature'
    
    '3-hour maximum 2-meter temperature'
    
    '6-hour minimum 2-meter temperature'
    
    '6-hour maximum 2-meter temperature'
    
    'total precipitation rate'
    
    'precipitation type'
    
    'top net longwave thermal radiation'
    
    'snow density'
    
    'surface net longwave thermal radiation'
    
    'surface net shortwave solar radiation'
    
    'surface shortwave radiation downward'
    
    'surface longwave radiation downward'
    
    'northward turbulent surface stress'
    
    'eastward turbulent surface stress'
    
    'eastward surface sea water velocity'
    
    'northward surface sea water velocity'
    
    'sea ice thickness'
    
    'sea surface height'
    
    'divergence'
    
    'geopotential height'
    
    'specific humidity'
    
    'relative humidity'
    
    'temperature'
    
    'u-wind component'
    
    'v-wind component'
    
    'vertical velocity'
    
    'relative vorticity'
        
    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 1150, 100, 50])
                            
    Here is a sample of how to query geopotential height and temperature at 850 and 500mb 
    
    `wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 850 -l 500`
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    ***Level Types***
    
    pressure
    
    surface
    
    soil
    
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-ecmwf ifs latest -v geopotential height -l 500 --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GFS0P25/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=ecmwf_ifs.nc)
    
    """
    
@ifs.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=360,
    show_default=True,
    type=int,
    help=("""This is the final forecast hour requested in the dataset. Default=360.
          
            00z & 12z Runs Have 360 hours
            
            06z & 18z Runs Have 144 hours
          
          """)
)

@_click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    type=bool,
    help="To clear your recycle bin with each run of the script set to True."
)

@_click.option(
    "--custom_directory",
    "-cdir",
    default="none",
    show_default=True,
    type=str,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@_click.option(
    "--clear_data",
    "-cd",
    default=False,
    show_default=True,
    type=bool,
    help="To bypass the safety scanner set --clear data to False: -cd False."
)

@_click.option(
    "--source",
    "-s",
    default="ecmwf",
    show_default=True,
    type=str,
    help="Default ecmwf is for ECMWF Open-Data - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
)

@_click.option(
    "--convert_temperature",
    "-ct",
    default=True,
    show_default=True,
    type=bool,
    help="When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit."
)

@_click.option(
    "--convert_to",
    "-tu",
    default='celsius',
    show_default=True,
    type=str,
    help="When -ct True this is where you declare the units for temperature to be converted to."
)

@_click.option(
    "--western_bound",
    "-wb",
    default=-180,
    show_default=True,
    type=int,
    help="Western Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=-180."
)

@_click.option(
    "--eastern_bound",
    "-eb",
    default=180,
    show_default=True,
    type=int,
    help="Eastern Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=180."
)

@_click.option(
    "--northern_bound",
    "-nb",
    default=90,
    show_default=True,
    type=int,
    help="Northern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=90."
)

@_click.option(
    "--southern_bound",
    "-sb",
    default=-90,
    show_default=True,
    type=int,
    help="Southern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=-90."
)
        
@_click.option('--variables', 
              '-v', 
              default=['geopotential height',
                        'specific humidity',
                        'relative humidity',
                        'temperature',
                        'u-wind component',
                        'v-wind component'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000, 
            925, 
            850, 
            700, 
            600, 
            500, 
            400, 
            300, 
            250, 
            200, 
            150, 
            100, 
            50],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 50]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, surface, soil.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
          """)
)

@_click.option(
    "--proxy",
    default="none",
    show_default=True,
    type=str,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)

@_click.option(
    "--process",
    default=True,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will process the data in addition to downloading the data. (Default=True)
          """),
)

@_click.option(
    "--netcdf",
    default=False,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will create a netCDF (.nc) file for all the data ingested from the GRIB files.
          """),
)

@_click.option(
    "--ncdir",
    default=f"ECMWF IFS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"ecmwf_ifs.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def fetch_ifs(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variables,
                  levels,
                  level_type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound,
                  convert_temperature,
                  convert_to):
    
    if proxy == "none":
        proxy = None
    else:
        proxy = proxy
    
    if custom_directory.lower() == "none":
        custom_directory = None
    else:
        custom_directory = custom_directory
        if current_os == "Windows":
            custom_directory = custom_directory.replace('/', '\\')
        else:
            pass
        
    if netcdf == True:
        if current_os == "Windows":
            ncdir = ncdir.replace('/', '\\')
        else:
            pass
    
    vars_fixed = []
    for v in variables:
        v = v.replace('_', ' ')
        vars_fixed.append(v)
        
    level_type = level_type.replace('_', ' ')
    
    try:
        _fetch_ecmwf_ifs(final_forecast_hour=final_forecast_hour,
                         western_bound=western_bound,
                         eastern_bound=eastern_bound,
                         northern_bound=northern_bound,
                         southern_bound=southern_bound,
                         clear_data=clear_data,
                         clear_recycle_bin=clear_recycle_bin,
                         proxies=proxy,
                         source=source,
                         level_type=level_type,
                         levels=levels,
                         convert_temperature=convert_temperature,
                         convert_to=convert_to,
                         to_netcdf=netcdf,
                         netcdf_path=ncdir,
                         netcdf_filename=ncfname,
                         process_data=process,
                         return_values=False,
                         variables=vars_fixed)
        
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"ECMWF IFS latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"ECMWF IFS latest download complete, data files saved to ECMWF/IFS")
            else:
                _click.echo(rf"ECMWF IFS latest download complete, data files saved to ECMWF\IFS")
            
    except SystemExit as e:
        _command_error_message('ecmwf ifs')
        _sys.exit(1)
    
@ecmwf_data.group(name='ifs_ens')
def ifs_ens():
    
    """
    **Downloads The Latest ECMWF IFS Data**
    
    ***Valid Commands***
    
    -f = Final Forecast Hour (Default=360).
     
    00z & 12z Runs Have 360 hours
    
    06z & 18z Runs Have 144 hours
    
    -s = Source (Default=ecmwf). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices***
    
    ecmwf - ECMWF Open-Data
    
    aws - Amazon Web Services
    
    google - Google Cloud Servers
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:ECMWF/IFS. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variables(Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 
                       
    The list of variables the user wants to query.
    
    Here is a sample of how to query geopotential height and temperature at 500mb `wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 500`
    
    ***Variable List***
    
    'Geopotential (step 0)'
    
    'Standard deviation of sub-gridscale orography (step 0)'
    
    '10-meter u-wind component'
    
    '10-meter v-wind component'
    
    '100-meter u-wind component'
    
    '100-meter v-wind component'
    
    'maximum 10-meter wind gust step 0'
    
    'maximum 10-meter wind gust steps 3-144'
    
    '2-meter temperature'
    
    '2-meter dewpoint temperature'
    
    'mean sea level pressure'
    
    'mean zero-crossing wave period'
    
    'mean wave direction'
    
    'mean wave period'
    
    'peak wave period'
    
    'significant wave height'
    
    'runoff'
    
    'total precipitation'
    
    'surface pressure'
    
    'total column vertically integrated water vapor'
    
    'total cloud cover'
    
    'snow depth water equivalent'
    
    'snowfall water equivalent'
    
    'land sea mask'
    
    'volumetric soil moisture content'
    
    'soil temperature'
    
    'most unstable cape'
    
    'snow albedo'
    
    '3-hour minimum 2-meter temperature'
    
    '3-hour maximum 2-meter temperature'
    
    '6-hour minimum 2-meter temperature'
    
    '6-hour maximum 2-meter temperature'
    
    'total precipitation rate'
    
    'precipitation type'
    
    'top net longwave thermal radiation'
    
    'snow density'
    
    'surface net longwave thermal radiation'
    
    'surface net shortwave solar radiation'
    
    'surface shortwave radiation downward'
    
    'surface longwave radiation downward'
    
    'northward turbulent surface stress'
    
    'eastward turbulent surface stress'
    
    'eastward surface sea water velocity'
    
    'northward surface sea water velocity'
    
    'sea ice thickness'
    
    'sea surface height'
    
    'divergence'
    
    'geopotential height'
    
    'specific humidity'
    
    'relative humidity'
    
    'temperature'
    
    'u-wind component'
    
    'v-wind component'
    
    'vertical velocity'
    
    'relative vorticity'
        
    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 1150, 100, 50])
                            
    Here is a sample of how to query geopotential height and temperature at 850 and 500mb 
    
    `wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 850 -l 500`
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    ***Level Types***
    
    pressure
    
    surface
    
    soil
    
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-ecmwf ifs latest -v geopotential height -l 500 --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GFS0P25/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=ecmwf_ifs.nc)
    
    """
    
@ifs_ens.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=360,
    show_default=True,
    type=int,
    help=("""This is the final forecast hour requested in the dataset. Default=360.
          
            00z & 12z Runs Have 360 hours
            
            06z & 18z Runs Have 144 hours
          
          """)
)

@_click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    type=bool,
    help="To clear your recycle bin with each run of the script set to True."
)

@_click.option(
    "--custom_directory",
    "-cdir",
    default="none",
    show_default=True,
    type=str,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@_click.option(
    "--clear_data",
    "-cd",
    default=False,
    show_default=True,
    type=bool,
    help="To bypass the safety scanner set --clear data to False: -cd False."
)

@_click.option(
    "--source",
    "-s",
    default="ecmwf",
    show_default=True,
    type=str,
    help="Default ecmwf is for ECMWF Open-Data - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
)

@_click.option(
    "--convert_temperature",
    "-ct",
    default=True,
    show_default=True,
    type=bool,
    help="When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit."
)

@_click.option(
    "--convert_to",
    "-tu",
    default='celsius',
    show_default=True,
    type=str,
    help="When -ct True this is where you declare the units for temperature to be converted to."
)

@_click.option(
    "--western_bound",
    "-wb",
    default=-180,
    show_default=True,
    type=int,
    help="Western Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=-180."
)

@_click.option(
    "--eastern_bound",
    "-eb",
    default=180,
    show_default=True,
    type=int,
    help="Eastern Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=180."
)

@_click.option(
    "--northern_bound",
    "-nb",
    default=90,
    show_default=True,
    type=int,
    help="Northern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=90."
)

@_click.option(
    "--southern_bound",
    "-sb",
    default=-90,
    show_default=True,
    type=int,
    help="Southern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=-90."
)
        
@_click.option('--variables', 
              '-v', 
              default=['geopotential height',
                        'specific humidity',
                        'relative humidity',
                        'temperature',
                        'u-wind component',
                        'v-wind component'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000, 
            925, 
            850, 
            700, 
            600, 
            500, 
            400, 
            300, 
            250, 
            200, 
            150, 
            100, 
            50],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 50]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, surface, soil.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
          """)
)

@_click.option(
    "--members",
    "-m",
    default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
            41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
    multiple=True,
    show_default=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 50 members.
    
            This is only necessary when category=members -> `-c members`
    
    """
)

@_click.option(
    "--proxy",
    default="none",
    show_default=True,
    type=str,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)

@_click.option(
    "--process",
    default=True,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will process the data in addition to downloading the data. (Default=True)
          """),
)

@_click.option(
    "--netcdf",
    default=False,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will create a netCDF (.nc) file for all the data ingested from the GRIB files.
          """),
)

@_click.option(
    "--ncdir",
    default=f"ECMWF IFS ENSEMBLE/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"ecmwf_ifs_ens.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def fetch_ifs_ens(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variables,
                  members,
                  levels,
                  level_type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound,
                  convert_temperature,
                  convert_to):
    
    if proxy == "none":
        proxy = None
    else:
        proxy = proxy
    
    if custom_directory.lower() == "none":
        custom_directory = None
    else:
        custom_directory = custom_directory
        if current_os == "Windows":
            custom_directory = custom_directory.replace('/', '\\')
        else:
            pass
        
    if netcdf == True:
        if current_os == "Windows":
            ncdir = ncdir.replace('/', '\\')
        else:
            pass
    
    vars_fixed = []
    for v in variables:
        v = v.replace('_', ' ')
        vars_fixed.append(v)
        
    level_type = level_type.replace('_', ' ')
    
    try:
        _fetch_ecmwf_ifs_ens(final_forecast_hour=final_forecast_hour,
                         western_bound=western_bound,
                         eastern_bound=eastern_bound,
                         northern_bound=northern_bound,
                         southern_bound=southern_bound,
                         clear_data=clear_data,
                         clear_recycle_bin=clear_recycle_bin,
                         proxies=proxy,
                         source=source,
                         level_type=level_type,
                         levels=levels,
                         members=members,
                         convert_temperature=convert_temperature,
                         convert_to=convert_to,
                         to_netcdf=netcdf,
                         netcdf_path=ncdir,
                         netcdf_filename=ncfname,
                         process_data=process,
                         return_values=False,
                         variables=vars_fixed)
        
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"ECMWF IFS Ensemble latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"ECMWF IFS Ensemble latest download complete, data files saved to ECMWF/IFS ENS")
            else:
                _click.echo(rf"ECMWF IFS Ensemble latest download complete, data files saved to ECMWF\IFS ENS")
            
    except SystemExit as e:
        _command_error_message('ecmwf ifs ens')
        _sys.exit(1)
    
@ecmwf_data.group(name='aifs')
def aifs():
    
    """
    **Downloads The Latest ECMWF AIFS Data**
    
    ***Valid Commands***
    
    -f = Final Forecast Hour (Default=360).
    
    -s = Source (Default=ecmwf). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices***
    
    ecmwf - ECMWF Open-Data
    
    aws - Amazon Web Services
    
    google - Google Cloud Servers
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:ECMWF/AIFS. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variables(Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 
                       
    The list of variables the user wants to query.
    
    Here is a sample of how to query geopotential height and temperature at 500mb `wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 500`
    
    ***Variable List***
    
    'Geopotential (step 0)'
    
    'Standard deviation of sub-gridscale orography (step 0)'
    
    '10-meter u-wind component'
    
    '10-meter v-wind component'
    
    '100-meter u-wind component'
    
    '100-meter v-wind component'
    
    'maximum 10-meter wind gust step 0'
    
    'maximum 10-meter wind gust steps 3-144'
    
    '2-meter temperature'
    
    '2-meter dewpoint temperature'
    
    'mean sea level pressure'
    
    'mean zero-crossing wave period'
    
    'mean wave direction'
    
    'mean wave period'
    
    'peak wave period'
    
    'significant wave height'
    
    'runoff'
    
    'total precipitation'
    
    'surface pressure'
    
    'total column vertically integrated water vapor'
    
    'total cloud cover'
    
    'snow depth water equivalent'
    
    'snowfall water equivalent'
    
    'land sea mask'
    
    'volumetric soil moisture content'
    
    'soil temperature'
    
    'most unstable cape'
    
    'snow albedo'
    
    '3-hour minimum 2-meter temperature'
    
    '3-hour maximum 2-meter temperature'
    
    '6-hour minimum 2-meter temperature'
    
    '6-hour maximum 2-meter temperature'
    
    'total precipitation rate'
    
    'precipitation type'
    
    'top net longwave thermal radiation'
    
    'snow density'
    
    'surface net longwave thermal radiation'
    
    'surface net shortwave solar radiation'
    
    'surface shortwave radiation downward'
    
    'surface longwave radiation downward'
    
    'northward turbulent surface stress'
    
    'eastward turbulent surface stress'
    
    'eastward surface sea water velocity'
    
    'northward surface sea water velocity'
    
    'sea ice thickness'
    
    'sea surface height'
    
    'divergence'
    
    'geopotential height'
    
    'specific humidity'
    
    'relative humidity'
    
    'temperature'
    
    'u-wind component'
    
    'v-wind component'
    
    'vertical velocity'
    
    'relative vorticity'
        
    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 1150, 100, 50])
                            
    Here is a sample of how to query geopotential height and temperature at 850 and 500mb 
    
    `wxdata-ecmwf ifs latest -v geopotential_height -v temperature -l 850 -l 500`
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    ***Level Types***
    
    pressure
    
    surface
    
    soil
    
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-ecmwf ifs latest -v geopotential height -l 500 --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GFS0P25/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=ecmwf_ifs.nc)
    
    """
    
@aifs.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=360,
    show_default=True,
    type=int,
    help=("""This is the final forecast hour requested in the dataset. Default=360.""")
)

@_click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    type=bool,
    help="To clear your recycle bin with each run of the script set to True."
)

@_click.option(
    "--custom_directory",
    "-cdir",
    default="none",
    show_default=True,
    type=str,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@_click.option(
    "--clear_data",
    "-cd",
    default=False,
    show_default=True,
    type=bool,
    help="To bypass the safety scanner set --clear data to False: -cd False."
)

@_click.option(
    "--source",
    "-s",
    default="ecmwf",
    show_default=True,
    type=str,
    help="Default ecmwf is for ECMWF Open-Data - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
)

@_click.option(
    "--convert_temperature",
    "-ct",
    default=True,
    show_default=True,
    type=bool,
    help="When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit."
)

@_click.option(
    "--convert_to",
    "-tu",
    default='celsius',
    show_default=True,
    type=str,
    help="When -ct True this is where you declare the units for temperature to be converted to."
)

@_click.option(
    "--western_bound",
    "-wb",
    default=-180,
    show_default=True,
    type=int,
    help="Western Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=-180."
)

@_click.option(
    "--eastern_bound",
    "-eb",
    default=180,
    show_default=True,
    type=int,
    help="Eastern Bound for subsetting the data. Range: -180 to 180 in Degrees Longitude. Default=180."
)

@_click.option(
    "--northern_bound",
    "-nb",
    default=90,
    show_default=True,
    type=int,
    help="Northern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=90."
)

@_click.option(
    "--southern_bound",
    "-sb",
    default=-90,
    show_default=True,
    type=int,
    help="Southern Bound for subsetting the data. Range: -90 to 90 in Degrees Latitude. Default=-90."
)
        
@_click.option('--variables', 
              '-v', 
              default=['geopotential height',
                        'specific humidity',
                        'relative humidity',
                        'temperature',
                        'u-wind component',
                        'v-wind component'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'specific humidity', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000, 
            925, 
            850, 
            700, 
            600, 
            500, 
            400, 
            300, 
            250, 
            200, 
            150, 
            100, 
            50],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 50]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, surface, soil.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
          """)
)

@_click.option(
    "--proxy",
    default="none",
    show_default=True,
    type=str,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)

@_click.option(
    "--process",
    default=True,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will process the data in addition to downloading the data. (Default=True)
          """),
)

@_click.option(
    "--netcdf",
    default=False,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will create a netCDF (.nc) file for all the data ingested from the GRIB files.
          """),
)

@_click.option(
    "--ncdir",
    default=f"ECMWF AIFS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"ecmwf_aifs.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def fetch_aifs(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variables,
                  levels,
                  level_type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound,
                  convert_temperature,
                  convert_to):
    
    if proxy == "none":
        proxy = None
    else:
        proxy = proxy
    
    if custom_directory.lower() == "none":
        custom_directory = None
    else:
        custom_directory = custom_directory
        if current_os == "Windows":
            custom_directory = custom_directory.replace('/', '\\')
        else:
            pass
        
    if netcdf == True:
        if current_os == "Windows":
            ncdir = ncdir.replace('/', '\\')
        else:
            pass
    
    vars_fixed = []
    for v in variables:
        v = v.replace('_', ' ')
        vars_fixed.append(v)
        
    level_type = level_type.replace('_', ' ')
    
    try:
        _fetch_ecmwf_aifs(final_forecast_hour=final_forecast_hour,
                         western_bound=western_bound,
                         eastern_bound=eastern_bound,
                         northern_bound=northern_bound,
                         southern_bound=southern_bound,
                         clear_data=clear_data,
                         clear_recycle_bin=clear_recycle_bin,
                         proxies=proxy,
                         source=source,
                         level_type=level_type,
                         levels=levels,
                         convert_temperature=convert_temperature,
                         convert_to=convert_to,
                         to_netcdf=netcdf,
                         netcdf_path=ncdir,
                         netcdf_filename=ncfname,
                         process_data=process,
                         return_values=False,
                         variables=vars_fixed)
        
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"ECMWF AIFS latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"ECMWF AIFS latest download complete, data files saved to ECMWF/AIFS")
            else:
                _click.echo(rf"ECMWF AIFS latest download complete, data files saved to ECMWF\AIFS")
            
    except SystemExit as e:
        _command_error_message('ecmwf aifs')
        _sys.exit(1)
    
    
    

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    ecmwf_data()
    
if __name__ == "__main__":
    main()
    