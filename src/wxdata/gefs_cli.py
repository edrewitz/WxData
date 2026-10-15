"""
This file hosts the WxData Command Line Interface for retrieving Global Ensemble Forecast System (GEFS) Data.

Command Line Use: `wxdata-gefs **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from datetime import datetime as _datetime
from wxdata.model_data.noaa.gefs.gefs import(
    gefs_0p50 as _fetch_gefs_0p50,
    gefs_0p50_secondary_parameters as _fetch_gefs_0p50_secondary_parameters,
    gefs_0p25 as _fetch_gefs_0p25
)
from wxdata.archived_data.model_data.noaa.gefs.gefs import(
    gefs_0p50 as _fetch_archived_gefs_0p50,
    gefs_0p50_secondary_parameters as _fetch_archived_gefs_0p50_secondary_parameters,
    gefs_0p25 as _fetch_archived_gefs_0p25
)

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
    print(f"Please run `wxdata-gefs -h to view the help documentation.")
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
def gefs_data():
    """GEFS command line utilities."""
    pass

# ---------------------------------------------------------------------
# GEFS 0.50x0.50 Commands
# ---------------------------------------------------------------------
@gefs_data.group(name='0p50')
def gefs0p50():
    """
    Global Ensemble Forecast System (GEFS) 0.50x0.50 Client.
    
    Archived Required Commands
    --------------------------
    
    -d = Date. The date of the model run in the format of YYYY-mm-dd.
    
        (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
        
    -r = Run. The model runtime in UTC (0, 6, 12, 18). 
    
        (i.e. for the 12z run set -r 12)
    
    
    Globally Valid Commands (valid for both "latest" and "archived")
    
    -------------------------------------------------------
    
    -t = type (Default=primary).
    
    This determines the type of variables and levels.
    
    -c = Category (Default='mean')
    
    This determines the category of ensemble data 
    
    Categories
    
    ----------
    
    1) mean
    
    2) members
    
    3) spread
    
    4) control
    
    -f = Final Forecast Hour (Default=384).
     
    The last hour the user wishes to download in the dataset. GEFS0P50 has 384 forecast hours.
    
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
    The default path is f:GEFS0P50/{CATEGORY}. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -wb = Western Bound - The western bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=-180)
    
    -eb = Eastern Bound - The eastern bound for subsetting the data range is from -180 to 180 degrees longitude. (Default=180)
    
    -nb = Northern Bound - The northern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=90)
    
    -sb = Southern Bound - The southern bound for subsetting the data range is from -90 to 90 degrees latitude. (Default=-90)
    
    -v = Variables(Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 
                       
    The list of variables the user wants to query.
    
    Here is a sample of how to query geopotential height and temperature `gefs 0p25 latest -v geopotential_height -v temperature`
    
    Primary Variables
    
    ------------------
    
    'total precipitation'
    
    'convective available potential energy'
    
    'categorical freezing rain'
    
    'categorical ice pellets'
    
    'categorical rain'
    
    'categorical snow'
    
    'convective inhibition'
    
    'downward longwave radiation flux'
    
    'downward shortwave radiation flux'
    
    'geopotential height'
    
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
    
    'vertical velocity'
    
    'water equivalent of accumulated snow depth'
    
    Secondary Variables
    
    -------------------
    
    'best lifted index'
    
    '5 wave geopotential height'
    
    'absolute vorticity'
    
    'temperature'
    
    'dew point'
    
    'convective precipitation'
    
    'albedo'
    
    'apparent temperature'
    
    'brightness temperature'
    
    'convective available potential energy'
    
    'clear sky uv-b downward solar flux'
    
    'convective inhibition'
    
    'cloud mixing ratio'
    
    'plant canopy surface water'
    
    'percent frozen precipitaion'
    
    'convective precipitation rate'
    
    'cloud water'
    
    'cloud work function'
    
    'uv-b downward solar flux'
    
    'field capacity'
    
    'surface friction velocity'
    
    'ground heat flux'
    
    'wind gust'
    
    'geopotential height'
    
    'haines index'
    
    'storm relative helicity'
    
    'planetary boundary layer height'
    
    'icao standard atmosphere reference height'
    
    'ice cover'
    
    'icing'
    
    'icing severity'
    
    'land cover'
    
    'surface lifted index'
    
    'montgomery stream function'
    
    'mslp (eta model reduction)'
    
    'large scale non-convective precipitation'
    
    'ozone mixing ratio'
    
    'potential evaporation rate'
    
    'parcel lifted index (to 500mb)'
    
    'pressure level from which parcel was lifted'
    
    'potential temperature'
    
    'precipitation rate'
    
    'pressure'
    
    'potential vorticity'
    
    'precipitable water'
    
    'relative humidity'
    
    'surface roughness'
    
    'snow phase-change heat flux'
    
    'snow cover'
    
    'liquid volumetric soil moisture (non-frozen)'
    
    'volumetric soil moisture content'
    
    'specific humidity'
    
    'sunshine duration'
    
    'total cloud cover'
    
    'total ozone'
    
    'soil temperature'
    
    'momentum flux (u-component)'
    
    'u-component of wind'
    
    'zonal flux of gravity wave stress'
    
    'u-component of storm motion'
    
    'upward shortwave radiation flux'
    
    'momentum flux (v-component)'
    
    'v-component of wind'
    
    'meridional flux of gravity wave stress'
    
    'visibility'
    
    'ventilation rate'
    
    'v-component of storm motion'
    
    'vertical velocity'
    
    'vertical speed shear'
    
    'water runoff'
    
    'wilting point'
    
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])
                            
    Here is a sample of how to query geopotential height and temperature at 850 and 500mb 
    
    `wxdata-gefs 0p50 latest -v geopotential_height -v temperature -l 850 -l 500`
    
    The default setting of levels assume pressure levels are being used and that the category is set to primary.
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    Primary Levels: 1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10
    
    Secondary Levels: Default=None -> level_type='surface'. 
    
    Example: level_type='height above ground' & levels=2 -> 2-meter above ground
                                                                
    Level Types
    
    -----------
    
    'pressure'
    
    'height below ground'
    
    'surface'
    
    'height above ground'
    
    'top of atmosphere'
    
    'pressure above ground'
    
    'mean sea level'

    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-gefs 0p25 latest -v geopotential height -l 500 --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GEFS0P50/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=gefs_0p50.nc)
    
    Commands Only Valid for "latest"
    --------------------------------
    
    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-gefs 0p50 latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data.     
    
    """
    
@gefs0p50.command("latest")
@_click.option(
    "--type",
    "-t",
    default="primary",
    type=str,
    show_default=True,
    help=("""This determines whether the user downloads primary or secondary data variables
          
          Default=primary
          
          set -t secondary for secondary variables.
          
          """
    )
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
            
            2) members
            
            3) spread
            
            4) control
    
          """
    )
)

@_click.option(
    "--final_forecast_hour",
    "-f",
    default=384,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
)

@_click.option(
    "--members",
    "-m",
    default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    show_default=True,
    multiple=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 30 members.
    
            This is only necessary when category=members -> `-c members`
    
    """
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
    default="noaa",
    show_default=True,
    type=str,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
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
              default=['geopotential_height',
                       'temperature',
                       'relative_humidity',
                       'u-component_of_wind'
                       'v-component_of_wind'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
                  See https://edrewitz.github.io/WxData/GEFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000,
            925,
            850,
            700,
            500,
            400,
            300,
            250,
            200,
            100,
            50,
            10],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10]
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available level types.
          
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
    default=f"GEFS0P50/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gefs_0p50.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def gefs0p50_fetch(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
                  source,
                  variables,
                  levels,
                  level_type,
                  category,
                  members,
                  type,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound):
    
    """Downloads Latest GEFS 0.50x0.50 Data"""
    
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
            vars_fixed.append(v)
            
        level_type = level_type.replace('_', ' ')
        
        category = category.lower()
        type = type.lower()
        
        if type == 'primary':
        
            _fetch_gefs_0p50(cat=category,
                             members=members,
                            final_forecast_hour=final_forecast_hour,
                            process_data=process,
                            proxies=proxy,
                            clear_recycle_bin=clear_recycle_bin,
                            custom_directory=custom_directory,
                            clear_data=clear_data,
                            source=source,
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
        else:
            
            _fetch_gefs_0p50_secondary_parameters(cat=category,
                                                  members=members,
                                                  final_forecast_hour=final_forecast_hour,
                                                    process_data=process,
                                                    proxies=proxy,
                                                    clear_recycle_bin=clear_recycle_bin,
                                                    custom_directory=custom_directory,
                                                    clear_data=clear_data,
                                                    source=source,
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
            _click.echo(f"GEFS0P50 {category.upper()} latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"GEFS0P50 {category.upper()} latest download complete, data files saved to GEFS0P50/ATMOSPHERIC")
            else:
                _click.echo(rf"GEFS0P50 {category.upper()} latest download complete, data files saved to GEFS0P50\ATMOSPHERIC")
            
    except SystemExit as e:
        _command_error_message('gefs0p50')
        _sys.exit(1)
        
        
@gefs0p50.command("archived")
@_click.option(
    "--date",
    "-d",
    type=str,
    help=("""This is a mandatory field. The date must be entered in the form of YYYY-mm-dd
          
          (i.e. December 25th, 2025 is 2025-12-25)
          
          """
    )
)

@_click.option(
    "--run",
    "-r",
    type=int,
    help=("""This is a mandatory field. The the model runtime must be entered as an integer corresponding to the run in UTC (0, 6, 12, 18)
                    
          """
    )
)

@_click.option(
    "--type",
    "-t",
    default="primary",
    type=str,
    show_default=True,
    help=("""This determines whether the user downloads primary or secondary data variables
          
          Default=primary
          
          set -t secondary for secondary variables.
          
          """
    )
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
            2) members
            3) spread
            4) control
    
          """
    )
)

@_click.option(
    "--members",
    "-m",
    default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    show_default=True,
    multiple=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 30 members.
    
            This is only necessary when category=members -> `-c members`
    
    """
)

@_click.option(
    "--final_forecast_hour",
    "-f",
    default=384,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
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
    default="GEFS0P50/Archive",
    show_default=True,
    type=str,
    help="The path of the directory where the archived GEFS0P25 data saves to."
)

@_click.option(
    "--source",
    "-s",
    default="aws",
    show_default=True,
    type=str,
    help="Default aws is for Amazon Web Services - set to google to switch to Google Cloud"
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
              default=['geopotential_height',
                       'temperature',
                       'relative_humidity',
                       'u-component_of_wind'
                       'v-component_of_wind'],
              multiple=True, 
              type=str,
              help=(
                  """"Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
                  See https://edrewitz.github.io/WxData/GEFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[1000,
            925,
            850,
            700,
            500,
            400,
            300,
            250,
            200,
            100,
            50,
            10],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Pressure (hPa)
          
          Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10]
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available level types.
          
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
    default=f"GEFS0P50/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gefs_0p50.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def archived_gefs0p50_fetch(
                  date,
                  run,
                  type,
                  members,
                  final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  source,
                  variables,
                  levels,
                  level_type,
                  category,
                  netcdf,
                  ncdir,
                  ncfname,
                  process,
                  western_bound,
                  eastern_bound,
                  northern_bound,
                  southern_bound):
    
    """Downloads Archived GEFS 0.50x0.50 Data For A Specified Date and Run"""
    
    try:
        vars_fixed = []
        for v in variables:
            v = v.replace('_', ' ')
            vars_fixed.append(v)
            
        if current_os == "Windows":
            custom_directory = custom_directory.replace('/', '\\')
        else:
            pass
    
        if netcdf == True:
            if current_os == "Windows":
                ncdir = ncdir.replace('/', '\\')
            else:
                pass
        
        level_type = level_type.replace('_', ' ')
        
        category = category.lower()
        type = type.lower()
        
        if type == 'primary':
        
            _fetch_archived_gefs_0p50(
                            date,
                            run,
                            cat=category,
                            members=members,
                            path=custom_directory,
                            final_forecast_hour=final_forecast_hour,
                            process_data=process,
                            proxies=proxy,
                            clear_recycle_bin=clear_recycle_bin,
                            source=source,
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
            
        else:
            
            _fetch_archived_gefs_0p50_secondary_parameters(
                            date,
                            run,
                            cat=category,
                            members=members,
                            path=custom_directory,
                            final_forecast_hour=final_forecast_hour,
                            process_data=process,
                            proxies=proxy,
                            clear_recycle_bin=clear_recycle_bin,
                            source=source,
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
        
        d = _parse_date(date)
        _click.echo(f"GEFS0P50 {category.upper()} download for {d.strftime('%Y-%m-%d')} {run}z complete, data files saved to {custom_directory}")
            
    except SystemExit as e:
        _command_error_message('gefs0p50')
        _sys.exit(1)
        

# ---------------------------------------------------------------------
# GEFS 0.25x0.25 Commands
# ---------------------------------------------------------------------        
@gefs_data.group(name='0p25')
def gefs0p25():
    """
    Global Ensemble Forecast System (GEFS) 0.25x0.25 Client.
    
    **Archived Required Commands**

    -d = Date. The date of the model run in the format of YYYY-mm-dd.
    
        (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
        
    -r = Run. The model runtime in UTC (0, 6, 12, 18). 
    
        (i.e. for the 12z run set -r 12)
    
    
    **Globally Valid Commands (valid for both "latest" and "archived")**

    -c = Category (Default='mean')
    
    This determines the category of ensemble data 
    
    **Categories**

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
    
    **Variables**

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
                                                                
    **Level Types**

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
    
    **Commands Only Valid for "latest"**

    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-gefs 0p25 latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data.   
    
    """
    
@gefs0p25.command("latest")
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
            2) members
            3) spread
            4) control
    
          """
    )
)

@_click.option(
    "--members",
    "-m",
    default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    show_default=True,
    multiple=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 30 members.
    
            This is only necessary when category=members -> `-c members`
    
    """
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
    "--source",
    "-s",
    default="noaa",
    show_default=True,
    type=str,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
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
              default=['temperature'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['temperature']
                  
                  See https://edrewitz.github.io/WxData/GEFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[2],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Height Above Ground [m]
          
          Default=[2]
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="height above ground",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='height above ground'.
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available level types.
          
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
    default=f"GEFS0P25/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gefs_0p25.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def gefs0p25_fetch(members,
                   category,
                   final_forecast_hour,
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
                  southern_bound):
    
    """Downloads Latest GEFS 0.25x0.25 Data"""
    
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
            vars_fixed.append(v)
            
        level_type = level_type.replace('_', ' ')
        category = category.lower()        
        
        _fetch_gefs_0p25(cat=category,
                         members=members,
                        final_forecast_hour=final_forecast_hour,
                        process_data=process,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        custom_directory=custom_directory,
                        clear_data=clear_data,
                        source=source,
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
            _click.echo(f"GEFS0P25 latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"GEFS0P25 latest download complete, data files saved to GEFS0P25/ATMOSPHERIC")
            else:
                _click.echo(f"GEFS0P25 latest download complete, data files saved to GEFS0P25/ATMOSPHERIC")
            
    except SystemExit as e:
        _command_error_message('gefs0p25')
        _sys.exit(1)
        
@gefs0p25.command("archived")
@_click.option(
    "--date",
    "-d",
    type=str,
    help=("""This is a mandatory field. The date must be entered in the form of YYYY-mm-dd
          
          (i.e. December 25th, 2025 is 2025-12-25)
          
          """
    )
)

@_click.option(
    "--run",
    "-r",
    type=int,
    help=("""This is a mandatory field. The the model runtime must be entered as an integer corresponding to the run in UTC (0, 6, 12, 18)
                    
          """
    )
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
            
            2) members
            
            3) spread
            
            4) control
    
          """
    )
)

@_click.option(
    "--members",
    "-m",
    default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    multiple=True,
    show_default=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 30 members.
    
            This is only necessary when category=members -> `-c members`
    
    """
)

@_click.option(
    "--final_forecast_hour",
    "-f",
    default=240,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
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
    default="GEFS0P25/Archive",
    show_default=True,
    type=str,
    help="The path of the directory where the archived GEFS0P25 data saves to."
)

@_click.option(
    "--source",
    "-s",
    default="aws",
    show_default=True,
    type=str,
    help="Default aws is for Amazon Web Services - set to google to switch to Google Cloud"
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
              default=['temperature'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['temperature']
                  
                  See https://edrewitz.github.io/WxData/GEFS0P25 for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=[2],
    multiple=True, 
    type=int,  
    help=("""Levels for pressure, height, PVU etc. 
          
          Height Above Ground [m]
          
          Default=[2]
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="height_above_ground",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='height above ground'.
          
          See https://edrewitz.github.io/WxData/GEFS0P25 for available level types.
          
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
    default=f"GEFS0P25/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gefs_0p25.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def archived_gefs0p50_fetch(
                  date,
                  run,
                  category,
                  members,
                  final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
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
                  southern_bound):
    
    """Downloads Archived GEFS 0.25x0.25 Data For A Specified Date and Run"""
    
    try:
        vars_fixed = []
        for v in variables:
            v = v.replace('_', ' ')
            vars_fixed.append(v)
            
        if current_os == "Windows":
            custom_directory = custom_directory.replace('/', '\\')
        else:
            pass

        level_type = level_type.replace('_', ' ')
        category = category.lower()
        
        
        _fetch_archived_gefs_0p25(
                        date,
                        run,
                        cat=category,
                        members=members,
                        path=custom_directory,
                        final_forecast_hour=final_forecast_hour,
                        process_data=process,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        source=source,
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
        
        d = _parse_date(date)
        _click.echo(f"GEFS0P25 download for {d.strftime('%Y-%m-%d')} {run}z complete, data files saved to {custom_directory}")
            
    except SystemExit as e:
        _command_error_message('gefs0p25')
        _sys.exit(1)

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    gefs_data()
    
if __name__ == "__main__":
    main()