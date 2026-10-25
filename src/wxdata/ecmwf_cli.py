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
    ecmwf_ifs_wave as _fetch_ecmwf_ifs_wave,
    ecmwf_ifs_wave_ens as _fetch_ecmwf_ifs_wave_ens,
    ecmwf_high_res_ifs as _fetch_ecmwf_high_res_ifs,
    ecmwf_high_res_ifs_ens as _fetch_ecmwf_high_res_ifs_ens,
    ecmwf_high_res_ifs_wave as _fetch_ecmwf_high_res_ifs_wave,
    ecmwf_high_res_ifs_wave_ens as _fetch_ecmwf_high_res_ifs_wave_ens,
    ecmwf_aifs as _fetch_ecmwf_aifs,
    ecmwf_aifs_ens as _fetch_ecmwf_aifs_ens,
    ecmwf_aifs_wave as _fetch_ecmwf_aifs_wave,
    ecmwf_aifs_wave_ens as _fetch_ecmwf_aifs_wave_ens
)

def _ecmwf_wave_var_error(model):
    
    """Error Message for Invalid Variable ECMWF Wave Models"""
    
    model = model.lower()
    
    print(f"\n\nAnother potential reason for this error is an invalid variable.")
    print(f"Please review the valid variable list.")
    
    if model == 'ifs':
        
        print(f"""
              
        Error: User Entered an invalid variable for IFS Wave/IFS Ensemble Wave/High Resolution IFS Wave        
              
        ***Variable List (ECMWF IFS Wave/IFS Wave Ensemble/High Resolution IFS Wave)***
        
        'mean_zero-crossing_wave_period'
        
        'significant_height_of_combined_waves_and_swell'
        
        'mean_wave_direction'
        
        'peak_wave_period'
        
        'mean_wave_period'
        
        """)
        
    else:
        
        print(f"""   
              
        ***Variable List (For ECMWF AIFS Wave/AIFS Wave Ensemble Data)***
    
        'significant_height_of_combined_waves_and_swell'
        
        'mean_wave_direction'
        
        'mean_wave_period'
        
        """)


def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please run `wxdata-ifs -h to view the help documentation.")
    print(f"Please visit: https://github.com/edrewitz/WxData/wiki#ecmwf-open-data for full detailed documentation.")
    
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
def ecmwf_data():
    """ECMWF command line utilities."""
    pass

# ---------------------------------------------------------------------
# ECMWF IFS Commands
# ---------------------------------------------------------------------
@ecmwf_data.group(name='ifs')
def ifs():
    
    """
    **Downloads The Latest ECMWF IFS Data**
    
    ***Valid Commands***
    
    ***IMPORTANT: All Default Settings are geared towards IFS Deterministic***
    
    -t = Type of ECMWF IFS Data. (Default='d').
    
    ***Here are the various commands for the different ECMWF IFS Model Options***
    
    -d = Deterministic IFS (0.25x0.25 Degree)
    
    -e = IFS Ensemble (0.25x0.25 Degree)
    
    -wd = IFS Wave Deterministic (0.25x0.25 Degree)
    
    -we = IFS Wave Ensemble (0.25x0.25 Degree)
    
    -hd = High Resolution Deterministic IFS (0.10x0.10 Degree)
    
    -he = High Resolution IFS Ensemble (0.10x0.10 Degree)
    
    -hwd = High Resolution IFS Wave Deterministic (0.10x0.10 Degree)
    
    -hwe = High Resolution Wave IFS Ensemble (0.10x0.10 Degree)
    
    ***Example***
    
    Download the ECMWF High Resolution IFS Ensemble for 500mb and 850mb geopotential height and temperature for members 1 through 5 from Google Cloud.
    
    `wxdata-ecmwf ifs latest -t he -v geopotential_height -v temperature -l 850 -l 500 -m 1 -m 2 -m 3 -m 4 -m 5 -s google`
    
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
    
    ***Variable List (All Except for ECMWF IFS/High Resolution IFS Wave Data)***
            
    '10-meter_u-wind_component'

    '10-meter_v-wind_component'

    '100-meter_u-wind_component'

    '100-meter_v-wind_component'

    'maximum_10-meter_wind_gust_step_0'

    'maximum_10-meter_wind_gust_steps_3-144'

    '2-meter_temperature'

    '2-meter_dewpoint_temperature'

    'mean_sea_level_pressure'

    'mean_zero-crossing_wave_period'

    'mean_wave_direction'

    'mean_wave_period'

    'peak_wave_period'

    'significant_wave_height'

    'runoff'

    'total_precipitation'

    'surface_pressure'

    'total_column_vertically_integrated_water_vapor'

    'total_cloud_cover'

    'snow_depth_water_equivalent'

    'snowfall_water_equivalent'

    'land_sea_mask'

    'volumetric_soil_moisture_content'

    'soil_temperature'

    'most_unstable_cape'

    'snow_albedo'

    '3-hour_minimum_2-meter_temperature'

    '3-hour_maximum_2-meter_temperature'

    '6-hour_minimum_2-meter_temperature'

    '6-hour_maximum_2-meter_temperature'

    'total_precipitation_rate'

    'precipitation_type'

    'top_net_longwave_thermal_radiation'

    'snow_density'

    'surface_net_longwave_thermal_radiation'

    'surface_net_shortwave_solar_radiation'

    'surface_shortwave_radiation_downward'

    'surface_longwave_radiation_downward'

    'northward_turbulent_surface_stress'

    'eastward_turbulent_surface_stress'

    'eastward_surface_sea_water_velocity'

    'northward_surface_sea_water_velocity'

    'sea_ice_thickness'

    'sea_surface_height'

    'divergence'

    'geopotential_height'

    'specific_humidity'

    'relative_humidity'

    'temperature'

    'u-wind_component'

    'v-wind_component'

    'vertical_velocity'

    'relative_vorticity'
    
    ***Variable List (ECMWF IFS Wave/IFS Wave Ensemble/High Resolution IFS Wave)***
    
    'mean_zero-crossing_wave_period'
    'significant_height_of_combined_waves_and_swell'
    'mean_wave_direction'
    'peak_wave_period'
    'mean_wave_period'
        
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
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=ECMWF IFS/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=ecmwf_ifs.nc)
    
    """
    
@ifs.command("latest")
@_click.option(
    "--type",
    "-t",
    default="d",
    type=str,
    show_default=True,
    help=("""This flag selects the type of ECMWF IFS data to be retrieved. 
          
          ***Here are the various commands for the different ECMWF IFS Model Options***
          
          -d = Deterministic IFS (0.25x0.25 Degree)
          
          -e = IFS Ensemble (0.25x0.25 Degree)
          
          -wd = IFS Wave Deterministic (0.25x0.25 Degree)
          
          -we = IFS Wave Ensemble (0.25x0.25 Degree)
          
          -hd = High Resolution Deterministic IFS (0.10x0.10 Degree)
          
          -he = High Resolution IFS Ensemble (0.10x0.10 Degree)
          
          -hwd = High Resolution IFS Wave Deterministic (0.10x0.10 Degree)
          
          -hwe = High Resolution Wave IFS Ensemble (0.10x0.10 Degree)
          
          """
    )
)

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
                  
                  See https://edrewitz.github.io/WxData/ECMWF_IFS for available variables."""
                  
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
          
          See https://edrewitz.github.io/WxData/ECMWF_IFS for available levels.
          
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
    show_default=True,
    multiple=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 50 members.
    
        This is only necessary when -t e or -t he or -t hwe
        
    """
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, surface, soil.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/ECMWF_IFS for available level types.
          
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

def fetch_ifs(type,
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
                  southern_bound,
                  convert_temperature,
                  convert_to,
                  members):
    
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
        
    if type == 'd':        
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
                    _click.echo(f"ECMWF IFS latest download complete, data files saved to ECMWF/IFS/DETERMINISTIC")
                else:
                    _click.echo(rf"ECMWF IFS latest download complete, data files saved to ECMWF\IFS\DETERMINISTIC")
                
        except SystemExit as e:
            _command_error_message('ecmwf ifs')
            _sys.exit(1)
            
    elif type == 'fd':        
        try:
            _fetch_ecmwf_high_res_ifs(final_forecast_hour=final_forecast_hour,
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
                _click.echo(f"ECMWF High Resolution IFS latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF High Resolution IFS latest download complete, data files saved to ECMWF/IFS/HIGH RES {level_type.upper()}")
                else:
                    _click.echo(rf"ECMWF High Resolution IFS latest download complete, data files saved to ECMWF\IFS\HIGH RES {level_type.upper()}")
                
        except SystemExit as e:
            _command_error_message('high resolution ecmwf ifs')
            _sys.exit(1)
    
    elif type == 'e':
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
                            convert_temperature=convert_temperature,
                            convert_to=convert_to,
                            to_netcdf=netcdf,
                            netcdf_path=ncdir,
                            netcdf_filename=ncfname,
                            process_data=process,
                            return_values=False,
                            variables=vars_fixed,
                            members=members)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF IFS ENSEMBLE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF IFS ENSEMBLE latest download complete, data files saved to ECMWF/IFS/ENSEMBLE")
                else:
                    _click.echo(rf"ECMWF IFS ENSEMBLE latest download complete, data files saved to ECMWF\IFS\ENSEMBLE")
                
        except SystemExit as e:
            _command_error_message('ecmwf ifs ensemble')
            _sys.exit(1)
            
    elif type == 'he':
        try:
            _fetch_ecmwf_high_res_ifs_ens(final_forecast_hour=final_forecast_hour,
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
                            variables=vars_fixed,
                            members=members)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF High Resolution IFS ENSEMBLE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF High Resolution IFS ENSEMBLE latest download complete, data files saved to ECMWF/IFS/HIGH RES ENSEMBLE {level_type.upper()}")
                else:
                    _click.echo(rf"ECMWF High Resolution IFS ENSEMBLE latest download complete, data files saved to ECMWF\IFS\HIGH RES ENSEMBLE {level_type.upper()}")
                
        except SystemExit as e:
            _command_error_message('high resolution ecmwf ifs ensemble')
            _sys.exit(1)
            
    elif type == 'wd':
        try:
            _fetch_ecmwf_ifs_wave(final_forecast_hour=final_forecast_hour,
                            western_bound=western_bound,
                            eastern_bound=eastern_bound,
                            northern_bound=northern_bound,
                            southern_bound=southern_bound,
                            clear_data=clear_data,
                            clear_recycle_bin=clear_recycle_bin,
                            proxies=proxy,
                            source=source,
                            to_netcdf=netcdf,
                            netcdf_path=ncdir,
                            netcdf_filename=ncfname,
                            process_data=process,
                            return_values=False,
                            variables=vars_fixed)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF IFS WAVE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF IFS WAVE latest download complete, data files saved to ECMWF/IFS/WAVE")
                else:
                    _click.echo(rf"ECMWF IFS WAVE latest download complete, data files saved to ECMWF\IFS\WAVE")
                
        except SystemExit as e:
            _command_error_message('ecmwf ifs wave')
            _ecmwf_wave_var_error('ifs')
            _sys.exit(1)
            
    elif type == 'hwd':
        try:
            _fetch_ecmwf_high_res_ifs_wave(final_forecast_hour=final_forecast_hour,
                            western_bound=western_bound,
                            eastern_bound=eastern_bound,
                            northern_bound=northern_bound,
                            southern_bound=southern_bound,
                            clear_data=clear_data,
                            clear_recycle_bin=clear_recycle_bin,
                            proxies=proxy,
                            source=source,
                            to_netcdf=netcdf,
                            netcdf_path=ncdir,
                            netcdf_filename=ncfname,
                            process_data=process,
                            return_values=False,
                            variables=vars_fixed)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF High Resolution IFS WAVE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF High Resolution IFS WAVE latest download complete, data files saved to ECMWF/IFS/HIGH RES WAVE")
                else:
                    _click.echo(rf"ECMWF High Resolution IFS WAVE latest download complete, data files saved to ECMWF\IFS\HIGH RES WAVE")
                
        except SystemExit as e:
            _command_error_message('high resolution ecmwf ifs wave')
            _ecmwf_wave_var_error('ifs')
            _sys.exit(1)
            
    elif type == 'we':
        try:
            _fetch_ecmwf_ifs_wave_ens(final_forecast_hour=final_forecast_hour,
                            western_bound=western_bound,
                            eastern_bound=eastern_bound,
                            northern_bound=northern_bound,
                            southern_bound=southern_bound,
                            clear_data=clear_data,
                            clear_recycle_bin=clear_recycle_bin,
                            proxies=proxy,
                            source=source,
                            to_netcdf=netcdf,
                            netcdf_path=ncdir,
                            netcdf_filename=ncfname,
                            process_data=process,
                            return_values=False,
                            variables=vars_fixed,
                            members=members)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF IFS WAVE ENSEMBLE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF IFS WAVE ENSEMBLE latest download complete, data files saved to ECMWF/IFS/WAVE ENSEMBLE")
                else:
                    _click.echo(rf"ECMWF IFS WAVE ENSEMBLE latest download complete, data files saved to ECMWF\IFS\WAVE ENSEMBLE")
                
        except SystemExit as e:
            _command_error_message('ecmwf ifs wave ensemble')
            _ecmwf_wave_var_error('ifs')
            _sys.exit(1)
            
    elif type == 'hwe':
        try:
            _fetch_ecmwf_high_res_ifs_wave_ens(final_forecast_hour=final_forecast_hour,
                            western_bound=western_bound,
                            eastern_bound=eastern_bound,
                            northern_bound=northern_bound,
                            southern_bound=southern_bound,
                            clear_data=clear_data,
                            clear_recycle_bin=clear_recycle_bin,
                            proxies=proxy,
                            source=source,
                            to_netcdf=netcdf,
                            netcdf_path=ncdir,
                            netcdf_filename=ncfname,
                            process_data=process,
                            return_values=False,
                            variables=vars_fixed,
                            members=members)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF High Resolution IFS WAVE ENSEMBLE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF High Resolution IFS WAVE ENSEMBLE latest download complete, data files saved to ECMWF/IFS/HIGH RES WAVE ENSEMBLE")
                else:
                    _click.echo(rf"ECMWF High Resolution IFS WAVE ENSEMBLE latest download complete, data files saved to ECMWF\IFS\HIGH RES WAVE ENSEMBLE")
                
        except SystemExit as e:
            _command_error_message('high resolution ecmwf ifs wave ensemble')
            _ecmwf_wave_var_error('ifs')
            _sys.exit(1)
            
    else:
        print(f"Error: {type} is not a valid model type.")
        print(f"""***Valid Model Types***
              
          -d = Deterministic IFS (0.25x0.25 Degree)
          
          -e = IFS Ensemble (0.25x0.25 Degree)
          
          -wd = IFS Wave Deterministic (0.25x0.25 Degree)
          
          -we = IFS Wave Ensemble (0.25x0.25 Degree)
          
          -hd = High Resolution Deterministic IFS (0.10x0.10 Degree)
          
          -he = High Resolution IFS Ensemble (0.10x0.10 Degree)
          
          -hwd = High Resolution IFS Wave Deterministic (0.10x0.10 Degree)
          
          -hwe = High Resolution Wave IFS Ensemble (0.10x0.10 Degree)
              
              """)
        print("System Exit")
        _sys.exit(1)
        
        
        
# ---------------------------------------------------------------------
# ECMWF IFS Commands
# ---------------------------------------------------------------------
@ecmwf_data.group(name='aifs')
def aifs():
    
    """
    **Downloads The Latest ECMWF AIFS Data**
    
    ***Valid Commands***
    
    -t = Type of ECMWF AIFS Data. (Default='d').
    
    ***Here are the various commands for the different ECMWF AIFS Model Options***
    
    -d = Deterministic AIFS (0.25x0.25 Degree)
    
    -e = AIFS Ensemble (0.25x0.25 Degree)
    
    -wd = AIFS Wave Deterministic (0.25x0.25 Degree)
    
    -we = AIFS Wave Ensemble (0.25x0.25 Degree)
    
    ***Example***
    
    Download the ECMWF High Resolution AIFS Ensemble for 500mb and 850mb geopotential height and temperature for members 1 through 5 from Google Cloud.
    
    `wxdata-ecmwf aifs latest -t e -v geopotential_height -v temperature -l 850 -l 500 -m 1 -m 2 -m 3 -m 4 -m 5 -s google`
    
    -c = Category. (Default="control").
    
    ***Valid Categories***
    
    1) control
    
    2) members
    
    -f = Final Forecast Hour (Default=360).
     
     Maximum forecast hour is 360 hours. 
    
    -s = Source (Default=ecmwf). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    ***Server Choices***
    
    ecmwf - ECMWF Open-Data
    
    aws - Amazon Web Services
    
    google - Google Cloud Servers
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    
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
    
    ***Variable List (All Except for ECMWF AIFS Wave/AIFS Wave Ensemble Data)***
    
    '10-meter_u-wind_component'

    '10-meter_v-wind_component'

    '100-meter_u-wind_component'

    '100-meter_v-wind_component'

    'maximum_10-meter_wind_gust_step_0'

    'maximum_10-meter_wind_gust_steps_3-144'

    '2-meter_temperature'

    '2-meter_dewpoint_temperature'

    'mean_sea_level_pressure'

    'mean_zero-crossing_wave_period'

    'mean_wave_direction'

    'mean_wave_period'

    'peak_wave_period'

    'significant_wave_height'

    'runoff'

    'total_precipitation'

    'surface_pressure'

    'total_column_vertically_integrated_water_vapor'

    'total_cloud_cover'

    'snow_depth_water_equivalent'

    'snowfall_water_equivalent'

    'land_sea_mask'

    'volumetric_soil_moisture_content'

    'soil_temperature'

    'most_unstable_cape'

    'snow_albedo'

    '3-hour_minimum_2-meter_temperature'

    '3-hour_maximum_2-meter_temperature'

    '6-hour_minimum_2-meter_temperature'

    '6-hour_maximum_2-meter_temperature'

    'total_precipitation_rate'

    'precipitation_type'

    'top_net_longwave_thermal_radiation'

    'snow_density'

    'surface_net_longwave_thermal_radiation'

    'surface_net_shortwave_solar_radiation'

    'surface_shortwave_radiation_downward'

    'surface_longwave_radiation_downward'

    'northward_turbulent_surface_stress'

    'eastward_turbulent_surface_stress'

    'eastward_surface_sea_water_velocity'

    'northward_surface_sea_water_velocity'

    'sea_ice_thickness'

    'sea_surface_height'

    'divergence'

    'geopotential_height'

    'specific_humidity'

    'relative_humidity'

    'temperature'

    'u-wind_component'

    'v-wind_component'

    'vertical_velocity'

    'relative_vorticity'
    
    ***Variable List (For ECMWF AIFS Wave/AIFS Wave Ensemble Data)***
    
    'significant_height_of_combined_waves_and_swell'
    
    'mean_wave_direction'
    
    'mean_wave_period'
        
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
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=ECMWF AIFS/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=ecmwf_aifs.nc)
    
    """
    
@aifs.command("latest")
@_click.option(
    "--type",
    "-t",
    default="d",
    type=str,
    show_default=True,
    help=("""This flag selects the type of ECMWF AIFS data to be retrieved. 
          
          ***Here are the various commands for the different ECMWF AIFS Model Options***
          
          -d = Deterministic AIFS (0.25x0.25 Degree)
          
          -e = AIFS Ensemble (0.25x0.25 Degree)
          
          -wd = AIFS Wave Deterministic (0.25x0.25 Degree)
          
          -we = AIFS Wave Ensemble (0.25x0.25 Degree)
          
          """
    )
)

@_click.option(
    "--category",
    "-c",
    default="control",
    type=str,
    show_default=True,
    help=("""The category of the ensemble data. Default='control'.  
    
            ***Valid Categories***
            
            1) control
            
            2) members
            
          """
    )
)

@_click.option(
    "--final_forecast_hour",
    "-f",
    default=360,
    show_default=True,
    type=int,
    help=("""This is the final forecast hour requested in the dataset. Default=360.
          
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
                  
                  See https://edrewitz.github.io/WxData/ECMWF_AIFS for available variables."""
                  
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
          
          See https://edrewitz.github.io/WxData/ECMWF_AIFS for available levels.
          
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
    show_default=True,
    multiple=True,
    type=int,
    help="""The individual ensemble members to select. Defaults to all 50 members.
    
        This is only necessary when -t e or -t he or -t hwe
        
    """
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, surface, soil.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/ECMWF_AIFS for available level types.
          
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

def fetch_aifs(type,
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
                  southern_bound,
                  convert_temperature,
                  convert_to,
                  members,
                  category):
    
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
    
    category = category.lower()
    
    vars_fixed = []
    for v in variables:
        v = v.replace('_', ' ')
        vars_fixed.append(v)
        
    if type == 'd':        
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
                    _click.echo(f"ECMWF AIFS latest download complete, data files saved to ECMWF/AIFS/DETERMINISTIC")
                else:
                    _click.echo(rf"ECMWF AIFS latest download complete, data files saved to ECMWF\AIFS\DETERMINISTIC")
                
        except SystemExit as e:
            _command_error_message('ecmwf aifs')
            _sys.exit(1)
    
    elif type == 'e':
        try:
            _fetch_ecmwf_aifs_ens(final_forecast_hour=final_forecast_hour,
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
                            variables=vars_fixed,
                            members=members,
                            cat=category)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF AIFS ENSEMBLE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF AIFS ENSEMBLE latest download complete, data files saved to ECMWF/AIFS/ENSEMBLE {category.upper()}")
                else:
                    _click.echo(rf"ECMWF AIFS ENSEMBLE latest download complete, data files saved to ECMWF\AIFS\ENSEMBLE {category.upper()}")
                
        except SystemExit as e:
            _command_error_message('ecmwf aifs ensemble')
            _sys.exit(1)
            
    elif type == 'wd':
        try:
            _fetch_ecmwf_aifs_wave(final_forecast_hour=final_forecast_hour,
                            western_bound=western_bound,
                            eastern_bound=eastern_bound,
                            northern_bound=northern_bound,
                            southern_bound=southern_bound,
                            clear_data=clear_data,
                            clear_recycle_bin=clear_recycle_bin,
                            proxies=proxy,
                            source=source,
                            to_netcdf=netcdf,
                            netcdf_path=ncdir,
                            netcdf_filename=ncfname,
                            process_data=process,
                            return_values=False,
                            variables=vars_fixed)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF AIFS WAVE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF AIFS WAVE latest download complete, data files saved to ECMWF/AIFS/WAVE")
                else:
                    _click.echo(rf"ECMWF AIFS WAVE latest download complete, data files saved to ECMWF\AIFS\WAVE")
                
        except SystemExit as e:
            _command_error_message('ecmwf aifs wave')
            _ecmwf_wave_var_error('aifs')
            _sys.exit(1)
            
    elif type == 'we':
        try:
            _fetch_ecmwf_aifs_wave_ens(final_forecast_hour=final_forecast_hour,
                            western_bound=western_bound,
                            eastern_bound=eastern_bound,
                            northern_bound=northern_bound,
                            southern_bound=southern_bound,
                            clear_data=clear_data,
                            clear_recycle_bin=clear_recycle_bin,
                            proxies=proxy,
                            source=source,
                            to_netcdf=netcdf,
                            netcdf_path=ncdir,
                            netcdf_filename=ncfname,
                            process_data=process,
                            return_values=False,
                            variables=vars_fixed,
                            members=members,
                            cat=category)
            if custom_directory != "none" and custom_directory != None:
                _click.echo(f"ECMWF AIFS WAVE ENSEMBLE latest download complete, data files saved to {custom_directory}")
            else:
                if current_os != "Windows":
                    _click.echo(f"ECMWF AIFS WAVE ENSEMBLE latest download complete, data files saved to ECMWF/AIFS/WAVE ENSEMBLE {category.upper()}")
                else:
                    _click.echo(rf"ECMWF AIFS WAVE ENSEMBLE latest download complete, data files saved to ECMWF\AIFS\WAVE ENSEMBLE {category.upper()}")
                
        except SystemExit as e:
            _command_error_message('ecmwf aifs wave ensemble')
            _ecmwf_wave_var_error('aifs')
            _sys.exit(1)
            
    else:
        print(f"Error: {type} is not a valid model type.")
        print(f"""***Valid Model Types***
              
          -d = Deterministic AIFS (0.25x0.25 Degree)
          
          -e = AIFS Ensemble (0.25x0.25 Degree)
          
          -wd = AIFS Wave Deterministic (0.25x0.25 Degree)
          
          -we = AIFS Wave Ensemble (0.25x0.25 Degree)
              
              """)
        print("System Exit")
        _sys.exit(1)

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    ecmwf_data()
    
if __name__ == "__main__":
    main()
    