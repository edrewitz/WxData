"""
This file hosts the WxData Command Line Interface for retrieving Hybrid Global Ensemble Forecast System (HGEFS) Data.

Command Line Use: `wxdata-hgefs **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from datetime import datetime as _datetime
from wxdata.model_data.noaa.hgefs.hgefs import hgefs_mean_spread as _fetch_hgefs

def _parse_date(date):
    
    """Parses String Date Into DateTime Object"""
    
    if type(date) == type(_datetime.now()):
        date = date
    else:
        date = f"{date[0:4]}{date[5:7]}{date[8:10]}"
        date = _datetime.strptime(date, "%Y%m%d")
        
    return date

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-hgefs -h to view the help documentation.")
    print(f"Please visit: https://github.com/edrewitz/WxData/wiki#global-ensemble-forecast-system-gefs for full detailed documentation.")

def _parse_proxy(value):
    if value is None:
        return None

    else:
        # Accept either http://host:port or https://host:port
        return {
            "http": value,
            "https": value,
        }
        
# ---------------------------------------------------------------------
# Top-level CLI group
# ---------------------------------------------------------------------
@_click.group(context_settings={"help_option_names": ["-h", "--help"]})
def hgefs_data():
    """HGEFS command line utilities."""
    pass

# ---------------------------------------------------------------------
# GEFS 0.25x0.25 Commands
# ---------------------------------------------------------------------
def hgefs():
    """
    Hybrid Global Ensemble Forecast System (HGEFS) Client.
    
    
    Valid Commands
    
    --------------
    
    -c = Category (Default='mean')
    
    This determines the category of ensemble data 
    
    Categories
    
    ----------
    
    1) mean
    
    2) members
    
    3) spread
    
    4) control
    
    -f = Final Forecast Hour (Default=240).
     
    The last hour the user wishes to download in the dataset. GEFS0P25 has 240 forecast hours.
    
    -s = Source (Default=noaa). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices For Latest Data***
    
    noaa - NCEP/NOMADS
    
    aws - Amazon Web Services
    
    google - Google Cloud Servers
    
    ***Server Choices For Archived Data***
    
    aws - Amazon Web Services
    
    google - Google Cloud Servers
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:GEFS0P25/{CATEGORY}. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variables(Default=['temperature']) 
                       
    The list of variables the user wants to query.
    
    Here is a sample of how to query ensemble members 2-meter temperature and relative humidity and create a netCDF file:
    
    `wxdata-gefs 0p25 latest -c members -v geopotential_height -v temperature -l 2 --netcdf True --ncdir GEFS0P25/Members/NETCDF --ncfname gefs_t_rh.nc`
    
    Variables
    
    ---------
    
    'total precipitation'
    
    'convective available potential energy'
    
    'categorical freezing rain'
    
    'categorical ice pellets'
    
    'convective inhibition'
    
    'percent frozen precipitaion'
    
    'categorical rain'
    
    'categorical snow'
    
    'downward longwave radiation flux'
    
    'downward shortwave radiation flux'
    
    'dew point'
    
    'wind gust'
    
    'geopotential height'
    
    'storm relative helicity'
    
    'ice thickness'
    
    'latent heat net flux'
    
    'pressure'
    
    'mean sea level pressure'
    
    'precipitable water'
    
    'relative humidity'
    
    'sensible heat net flux'
    
    'snow depth'
    
    'volumetric soil moisture content'
    
    'total cloud cover'
    
    'maximum temperature'
    
    'minimum temperature'
    
    'temperature'
    
    'soil temperature'
    
    'u-component of wind'
    
    'upward longwave radiation flux'
    
    'upward shortwave radiation flux'
    
    'v-component of wind'
    
    'visibility'
    
    'water equivalent of accumulated snow depth'
    
    -l = Levels (Default=[2])
    
    The default setting of levels assume height above ground levels are being used and that the category is set to primary.
    
    -lt = Level Type (Default=height above ground).
    
    This corresponds to the type of level.
                                                                
    Level Types
    
    -----------
    
    'surface'
    
    'mean sea level'
    
    'height above ground'
    
    'height below ground'
    
    'entire atmosphere (considered as a single layer)'
    
    'cloud ceiling'
    
    'pressure above ground'

    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-gefs 0p25 latest -v temperature -l 2 --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GEFS0P25/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=gefs_0p25.nc)
    
    Commands Only Valid for "latest"
    --------------------------------
    
    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-gefs 0p25 latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data.   
    
    """
@hgefs.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=240,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
)

@_click.option(
    "--category",
    "-c",
    default="mean",
    type=str,
    show_default=True,
    help=("""The category of the ensemble data. Default='mean'.  
    
            Valid categories
            -----------------
            
            1) mean
                        
            2) spread
                
          """
    )
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
    help="To bypass the safety scanner set --clear data to False."
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
                       'temperature',
                       'u-component of_wind',
                       'v-component of_wind',
                       'vertical velocity'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential height',
                       'specific humidity',
                       'temperature',
                       'u-component of wind',
                       'v-component of wind',
                       'vertical velocity']
                  
                  See https://edrewitz.github.io/WxData/HGEFS for available variables."""
                  
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
            150,
            100,
            50],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure in hPa. 
          
          Default=[1000,
                    925,
                    850,
                    700,
                    600,
                    500,
                    400,
                    300,
                    250,
                    150,
                    100,
                    50]
          
          See https://edrewitz.github.io/WxData/HGEFS for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level: pressure or surface. 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/HGEFS for available level types.
          
          """)
)

@_click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
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
    default=f"HGEFS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"hgefs.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def hgefs_fetch(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
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
                  southern_bound):
    
    """Downloads Latest HGEFS Data"""
    
    try:
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
            if v == 'vertical velocity':
                v = 'vertical velocity (pressure)'
            else:
                v = v
            vars_fixed.append(v)
            
        level_type = level_type.replace('_', ' ')
        
        _fetch_hgefs(final_forecast_hour=final_forecast_hour,
                        process_data=process,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        custom_directory=custom_directory,
                        clear_data=clear_data,
                        variables=vars_fixed,
                        levels=levels,
                        level_type=level_type,
                        to_netcdf=netcdf,
                        netcdf_path=ncdir,
                        netcdf_filename=ncfname,
                        return_values=False,
                        western_bound=western_bound,
                        eastern_bound=eastern_bound,
                        northern_bound=northern_bound,
                        southern_bound=southern_bound)
        
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"HGEFS latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"HGEFS latest download complete, data files saved to GEFS0P25/ATMOSPHERIC")
            else:
                _click.echo(f"HGEFS latest download complete, data files saved to GEFS0P25/ATMOSPHERIC")
            
    except SystemExit as e:
        _command_error_message('hgefs')
        _sys.exit(1)
        

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    hgefs_data()
    
if __name__ == "__main__":
    main()