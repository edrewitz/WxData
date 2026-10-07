import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from datetime import datetime as _datetime
from wxdata.model_data.noaa.gfs.gfs import(
    gfs_0p25 as _fetch_gfs_0p25,
    gfs_0p25_secondary_parameters as _fetch_gfs_0p25_secondary_parameters,
    gfs_0p50 as _fetch_gfs_0p50
)

from wxdata.archived_data.model_data.noaa.gfs.gfs import(
    gfs_0p25 as _fetch_archived_gfs_0p25,
    gfs_0p25_secondary_parameters as _fetch_archived_gfs_0p25_secondary_parameters,
    gfs_0p50 as _fetch_archived_gfs_0p50
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
    print(f"Please run `gfs {model.lower()} -h to view the help documentation.")
    print(f"Please visit: https://github.com/edrewitz/WxData/wiki#global-forecast-system-gfs for full detailed documentation.")

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
def gfs_data():
    """GFS command line utilities."""
    pass

# ---------------------------------------------------------------------
# GFS 0.25x0.25 Commands
# ---------------------------------------------------------------------
@gfs_data.group(name='0p25')
def gfs0p25():
    """
    GFS 0.25x0.25 Client.
    
    Archived Required Commands
    --------------------------
    
    -d = Date. The date of the model run in the format of YYYY-mm-dd.
    
        (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
        
    -r = Run. The model runtime in UTC (0, 6, 12, 18). 
    
        (i.e. for the 12z run set -r 12)
    
    
    Globally Valid Commands (valid for both "latest" and "archived")
    
    -------------------------------------------------------
    
    -c = Category (Default=primary).
    
    This determines the category of variables and levels.
    
    -f = Final Forecast Hour (Default=384).
     
    The last hour the user wishes to download in the dataset. GFS0P25 has 384 forecast hours.
    
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
    The default path is f:GFS0P25/ATMOSPHERIC. 
    
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
    
    Here is a sample of how to query geopotential height and temperature `gfs 0p25 latest -v geopotential_height -v temperature`
    
    Primary Variables
    
    ------------------
    
    best_lifted_index
    
    absolute_vorticity
    
    convective_precipitation
    
    albedo
    
    total_precipitation
    
    convective_available_potential_energy
    
    categorical_freezing_rain
    
    categorical_ice_pellets
    
    convective_inhibition
    
    cloud_mixing_ratio
    
    plant_canopy_surface_water
    
    percent_frozen_precipitaion
    
    convective_precipitation_rate
    
    categorical_rain
    
    categorical_snow
    
    cloud_water
    
    cloud_work_function
    
    downward_longwave_radiation_flux
    
    dew_point
    
    downward_shortwave_radiation_flux
    
    vertical_velocity_(height)
    
    field_capacity
    
    surface_friction_velocity
    
    ground_heat_flux
    
    graupel
    
    wind_gust
    
    high_cloud_cover
    
    geopotential_height
    
    haines_index
    
    storm_relative_helicity
    
    planetary_boundary_layer_height
    
    icao_standard_atmosphere_reference_height
    
    ice_cover
    
    ice_growth_rate
    
    ice_thickness
    
    ice_temperature
    
    ice_water_mixing_ratio
    
    land_cover
    
    low_cloud_cover
    
    surface_lifted_index
    
    latent_heat_net_flux
    
    middle_cloud_cover
    
    mean_sea_level_pressure
    
    mslp_(eta_model_reduction)
    
    ozone_mixing_ratio
    
    potential_evaporation_rate
    
    pressure_level_from_which_parcel_was_lifted
    
    potential_temperature
    
    precipitation_rate
    
    pressure
    
    mean_sea_level_pressure
    
    precipitable_water
    
    composite_reflectivity
    
    reflectivity
    
    relative_humidity
    
    rain_mixing_ratio
    
    surface_roughness
    
    sensible_heat_net_flux
    
    snow_mixing_ratio
    
    snow_depth
    
    liquid_volumetric_soil_moisture_(non-frozen)
    
    volumetric_soil_moisture_content
    
    soil_type
    
    specific_humidity
    
    sunshine_duration
    
    total_cloud_cover
    
    maximum_temperature
    
    minimum_temperature
    
    temperature
    
    total_ozone
    
    soil_temperature
    
    momentum_flux_(u-component)
    
    u-component_of_wind
    
    zonal_flux_of_gravity_wave_stress
    
    upward_longwave_radiation_flux
    
    u-component_of_storm_motion
    
    upward_shortwave_radiation_flux
    
    vegetation
    
    momentum_flux_(v-component)
    
    v-component_of_wind
    
    meridional_flux_of_gravity_wave_stress
    
    visibility
    
    ventilation_rate
    
    v-component_of_storm_motion
    
    vertical_velocity_(pressure)
    
    vertical_speed_shear
    
    water_runoff
    
    lated_snow_depth
    
    wilting_point
    
    Secondary Variables
    
    -------------------
    
    absolute_vorticity

    clear_sky_uv-b_downward_solar_flux

    cloud_mixing_ratio

    plant_canopy_surface_water

    uv-b_downward_solar_flux

    vertical_velocity_(height)

    graupel

    geopotential_height

    ice_thickness

    ice_water_mixing_ratio

    ozone_mixing_ratio

    pressure

    relative_humidity

    rain_mixing_ratio

    snow_mixing_ratio

    liquid_volumetric_soil_moisture_(non-frozen)

    specific_humidity

    total_cloud_cover

    temperature

    u-component_of_wind

    v-component_of_wind

    vertical_velocity_(pressure)

    vertical_speed_shear
    
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])
                            
    
    Here is a sample of how to query geopotential height and temperature at 850 and 500mb 
    
    `wxdata-gfs 0p25 latest -v geopotential_height -v temperature -l 850 -l 500`
    
    The default setting of levels assume pressure levels are being used and that the category is set to primary.
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    Primary Levels: 1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10
    
    Secondary Levels: 875, 825, 775, 725, 675, 625, 575, 525, 475, 425, 375, 325, 275, 225, 175, 125, 7, 5, 3, 2, 1
    
    Level Types
    
    -----------
    
    pressure

    mean_sea_level

    hybrid

    entire_atmosphere

    boundary_layer

    low_cloud_layer

    middle_cloud_layer

    high_cloud_layer

    convective_cloud_bottom_level

    low_cloud_bottom_level

    middle_cloud_bottom_level

    high_cloud_bottom_level

    convective_cloud_top_level

    low_cloud_top_level

    middle_cloud_top_level

    high_cloud_top_level

    convective_cloud_layer

    tropopause

    max_wind

    isothermal

    highest_tropospheric_freezing_level

    height_above_ground

    surface

    height_below_ground

    sigma_layer

    sigma_level

    entire_atmosphere_(considered_as_a_single_layer)

    pressure_above_ground

    potential_vorticity_surface
    
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-gfs 0p25 latest -v geopotential height -l 500 --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GFS0P25/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=gfs_0p25.nc)
    
    Commands Only Valid for "latest"
    --------------------------------
    
    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-gfs 0p25 latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data. 
    
    """
    
@gfs0p25.command("latest")
@_click.option(
    "--category",
    "-c",
    default="primary",
    type=str,
    show_default=True,
    help=("""This determines whether the user downloads primary or secondary data variables
          
          Default=primary
          
          set -c secondary for secondary variables.
          
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"GFS0P25/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gfs_0p25.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def gfs0p25_fetch(final_forecast_hour,
                  proxy,
                  clear_recycle_bin,
                  custom_directory,
                  clear_data,
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
    
    """Downloads Latest GFS 0.25x0.25 Data"""
    
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
        
        if category == 'primary':
        
            _fetch_gfs_0p25(final_forecast_hour=final_forecast_hour,
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
            
            _fetch_gfs_0p25_secondary_parameters(final_forecast_hour=final_forecast_hour,
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
        
        if custom_directory != "none":
            _click.echo(f"GFS0P25 {category.upper()} latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"GFS0P25 {category.upper()} latest download complete, data files saved to GFS0P25/ATMOSPHERIC")
            else:
                _click.echo(rf"GFS0P25 {category.upper()} latest download complete, data files saved to GFS0P25\ATMOSPHERIC")
            
    except SystemExit as e:
        _command_error_message('gfs0p25')
        _sys.exit(1)
        
        
@gfs0p25.command("archived")
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
    default="primary",
    type=str,
    show_default=True,
    help=("""This determines whether the user downloads primary or secondary data variables
          
          Default=primary
          
          set -c secondary for secondary variables.
          
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
    default="GFS0P25/Archive",
    show_default=True,
    type=str,
    help="The path of the directory where the archived GFS0P25 data saves to."
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
                  """"Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"GFS0P25/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gfs_0p25.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def archived_gfs0p25_fetch(
                  date,
                  run,
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
    
    """Downloads Archived GFS 0.25x0.25 Data For A Specified Date and Run"""
    
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
        
        if category == 'primary':
        
            _fetch_archived_gfs_0p25(
                            date,
                            run,
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
            
            _fetch_archived_gfs_0p25_secondary_parameters(
                            date,
                            run,
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
        _click.echo(f"GFS0P25 {category.upper()} download for {d.strftime('%Y-%m-%d')} {run}z complete, data files saved to {custom_directory}")
            
    except SystemExit as e:
        _command_error_message('gfs0p25')
        _sys.exit(1)
        
        
@gfs_data.group(name='0p50')
def gfs0p50():
    """
    GFS 0.50x0.50 Client.
    
    Archived Required Commands
    --------------------------
    
    -d = Date. The date of the model run in the format of YYYY-mm-dd.
    
        (i.e. December 25th, 2025 should be entered as -d 2025-12-25)
        
    -r = Run. The model runtime in UTC (0, 6, 12, 18). 
    
        (i.e. for the 12z run set -r 12)
    
    
    Globally Valid Commands (valid for both "latest" and "archived")
    
    -------------------------------------------------------
    
    -f = Final Forecast Hour (Default=384).
     
    The last hour the user wishes to download in the dataset. GFS0P50 has 384 forecast hours.
    
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
    
    -cd = Clear Data (Default=False).
    
    ***Only for wxdata-gfs 0p50 latest***
    
    ***Archived Clients Automatically Clear Old Data***
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data. 
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:GFS0P50/ATMOSPHERIC. 
    
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
    
    Here is a sample of how to query geopotential height and temperature `gfs 0p50 latest -v geopotential_height -v temperature`
    
    Variables
    
    ---------
    
    best_lifted_index
    
    absolute_vorticity
    
    convective_precipitation
    
    albedo
    
    total_precipitation
    
    convective_available_potential_energy
    
    categorical_freezing_rain
    
    categorical_ice_pellets
    
    convective_inhibition
    
    cloud_mixing_ratio
    
    plant_canopy_surface_water
    
    percent_frozen_precipitaion
    
    convective_precipitation_rate
    
    categorical_rain
    
    categorical_snow
    
    cloud_water
    
    cloud_work_function
    
    downward_longwave_radiation_flux
    
    dew_point
    
    downward_shortwave_radiation_flux
    
    vertical_velocity_(height)
    
    field_capacity
    
    surface_friction_velocity
    
    ground_heat_flux
    
    graupel
    
    wind_gust
    
    high_cloud_cover
    
    geopotential_height
    
    haines_index
    
    storm_relative_helicity
    
    planetary_boundary_layer_height
    
    icao_standard_atmosphere_reference_height
    
    ice_cover
    
    ice_growth_rate
    
    ice_thickness
    
    ice_temperature
    
    ice_water_mixing_ratio
    
    land_cover
    
    low_cloud_cover
    
    surface_lifted_index
    
    latent_heat_net_flux
    
    middle_cloud_cover
    
    mean_sea_level_pressure
    
    mslp_(eta_model_reduction)
    
    ozone_mixing_ratio
    
    potential_evaporation_rate
    
    pressure_level_from_which_parcel_was_lifted
    
    potential_temperature
    
    precipitation_rate
    
    pressure
    
    mean_sea_level_pressure
    
    precipitable_water
    
    composite_reflectivity
    
    reflectivity
    
    relative_humidity
    
    rain_mixing_ratio
    
    surface_roughness
    
    sensible_heat_net_flux
    
    snow_mixing_ratio
    
    snow_depth
    
    liquid_volumetric_soil_moisture_(non-frozen)
    
    volumetric_soil_moisture_content
    
    soil_type
    
    specific_humidity
    
    sunshine_duration
    
    total_cloud_cover
    
    maximum_temperature
    
    minimum_temperature
    
    temperature
    
    total_ozone
    
    soil_temperature
    
    momentum_flux_(u-component)
    
    u-component_of_wind
    
    zonal_flux_of_gravity_wave_stress
    
    upward_longwave_radiation_flux
    
    u-component_of_storm_motion
    
    upward_shortwave_radiation_flux
    
    vegetation
    
    momentum_flux_(v-component)
    
    v-component_of_wind
    
    meridional_flux_of_gravity_wave_stress
    
    visibility
    
    ventilation_rate
    
    v-component_of_storm_motion
    
    vertical_velocity_(pressure)
    
    vertical_speed_shear
    
    water_runoff
    
    lated_snow_depth
    
    wilting_point
    
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])
                            
    
    Here is a sample of how to query geopotential height and temperature at 850 and 500mb 
    
    `wxdata-gfs 0p50 latest -v geopotential_height -v temperature -l 850 -l 500`
    
    The default setting of levels assume pressure levels are being used and that the category is set to primary.
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
    Levels: 1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10
    
    
    Level Types
    
    -----------
    
    pressure

    mean_sea_level

    hybrid

    entire_atmosphere

    boundary_layer

    low_cloud_layer

    middle_cloud_layer

    high_cloud_layer

    convective_cloud_bottom_level
    
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: 
    
    `wxdata-gfs 0p50 latest -v geopotential height -l 500 --proxy https://proxy-server-address:proxy-server-port`
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    **Additional Relevant Flags when --netcdf True**
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=GFS0P50/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=gfs_0p50.nc)
    
    """
    
@gfs0p50.command("latest")
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"GFS0P50/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gfs_0p50.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def gfs0p50_fetch(final_forecast_hour,
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
    
    """Downloads Latest GFS 0.50x0.50 Data"""
    
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
                
        
        _fetch_gfs_0p50(final_forecast_hour=final_forecast_hour,
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
        
        if custom_directory != "none":
            _click.echo(f"GFS0P50 latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"GFS0P50 latest download complete, data files saved to GFS0P50/ATMOSPHERIC")
            else:
                _click.echo(f"GFS0P50 latest download complete, data files saved to GFS0P50/ATMOSPHERIC")
            
    except SystemExit as e:
        _command_error_message('gfs0p50')
        _sys.exit(1)
        
@gfs0p50.command("archived")
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
    default="GFS0P50/Archive",
    show_default=True,
    type=str,
    help="The path of the directory where the archived GFS0P25 data saves to."
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
                  """"Variables to pass into the function. 
                  
                  Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']
                  
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
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
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
    default=f"GFS0P50/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"gfs_0p50.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def archived_gfs0p50_fetch(
                  date,
                  run,
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
    
    """Downloads Archived GFS 0.50x0.50 Data For A Specified Date and Run"""
    
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
        
        
        
        _fetch_archived_gfs_0p50(
                        date,
                        run,
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
        _click.echo(f"GFS0P50 download for {d.strftime('%Y-%m-%d')} {run}z complete, data files saved to {custom_directory}")
            
    except SystemExit as e:
        _command_error_message('gfs0p50')
        _sys.exit(1)

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    gfs_data()
    
if __name__ == "__main__":
    main()