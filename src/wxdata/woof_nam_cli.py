"""
This file hosts the WxData Command Line Interface for retrieving the Open Source WOOF-NAM CONUS Data.

Command Line Use: `wxdata-woof-nam **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.recast_systems.woof_nam import woof_nam as _fetch_woof_nam

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please visit: https://edrewitz.github.io/WxData/WOOF-NAM%20CLI for full detailed documentation.")

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
def woof_nam_data():
    """WOOF-NAM command line utilities."""
    pass

# ---------------------------------------------------------------------
# WOOF-NAM Commands
# ---------------------------------------------------------------------
@woof_nam_data.group(name='fetch')
def woof_nam():
    
    r"""
    WOOF-NAM Client.
    
    ***Valid Commands***
        
    -f = Final Forecast Hour (Default=84).
     
    The last hour the user wishes to download in the dataset. WOOF-NAM has 84 forecast hours.
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cdir directory_branch_path.
    The default path is f:WOOF-NAM. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -cd = Clear Data (Default=False).
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data.   
    
    -v = Variables(Default=['geopotential height',
                        'temperature',
                        'relative humidity',
                        'vertical velocity (pressure)',
                        'vertical velocity (height)',
                        'u-component of wind',
                        'v-component of wind',
                        'turbulent kinetic energy']) 
                       
    The list of variables the user wants to query.
    
    ***Variables***
    
    'mean_sea_level_pressure'

    'reflectivity'

    'composite_reflectivity'

    'visibility'

    'geopotential_height'

    'u-component_of_wind'

    'v-component_of_wind'

    'temperature'

    'ventilation_rate'

    'wind_gust'

    'radar_echo_top_height'

    'vertical_velocity_height'

    'relative_humidity'

    'specific_humidity'

    'vertical_velocity_pressure'

    'turbulent_kinetic_energy'

    'mslp_eta_reduction'

    'soil_temperature'

    'volumetric_soil_moisture_content'

    'liquid_volumetric_soil_moisture_non-frozen'

    'soil_moisture_content'

    'soil_porosity'

    'number_of_soil_layers'

    'haines_index'

    'absolute_vorticity'

    'moisture_availability'

    'plant_canopy_surface_water'

    'water_equivalent_of_accumulated_snow_depth'

    'snow_cover'

    'snow_depth'

    'direct_evaporation_cease'

    'dew_point'

    'total_precipitation'

    'convective_precipitation'

    'water_equivalent_of_accumulated_snow_depth'

    'categorical_snow'

    'categorical_ice_pellets'

    'categorical_freezing_rain'

    'categorical_rain'

    'surface_roughness'

    'surface_friction_velocity'

    'drag_coefficient'

    'vegetation'

    'vegetation_type'

    'wilting_point'

    'transpiration_stress_onset'

    'surface_lifted_index'

    'best_lifted_index'

    'convective_available_potential_energy'

    'convective_inhibition'

    'storm_relative_helicity'

    'vertical_shear_u-component'

    'vertical_shear_v-component'

    'pressure'

    'parcel_lifted_index'

    'planetary_boundary_layer_height'

    'land_cover'

    'ice_cover'

    'albedo'

    'sensible_heat_net_flux'

    'latent_heat_net_flux'

    'total_cloud_cover'

    'downward_shortwave_radiation_flux'

    'downward_longwave_radiation_flux'

    'upward_shortwave_radiation_flux'

    'upward_longwave_radiation_flux'
    
    -l = Levels (Default=[1000,
                            925,
                            850,
                            700,
                            500,
                            300,
                            250,
                            100,
                            50])
    
    The default setting of levels assume height above ground levels are being used and that the category is set to primary.
    
    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -lt = Level Type (Default=height above ground).
    
    This corresponds to the type of level.
                                                                
    ***Level Types***
    
    'mean_sea_level'

    'hybrid'

    'entire_atmosphere_single_layer'

    'surface'

    'boundary_layer'

    'pressure'

    'height_above_ground'

    'depth_below_land_layer'

    'height_below_ground'

    'lowest_level_wetbulb_zero'

    'isobaric_layer'

    'cloud_base'

    'height_above_ground_layer_helicity'

    'height_above_ground_layer_shear'

    'tropopause'

    'max_wind'

    'isothermal'

    'pressure_above_ground'

    'sigma_layer'

    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    ***Additional Relevant Flags when --netcdf True***
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=WOOF-NAM/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=woof_nam.nc)
    
    ***Complex Example***
    
    *Important*: Any parameter of the command not explicitly stated results in the default value being used. 
    
    1) Download the latest WOOF-NAM for 500mb Geopotential Height
     
        - Use a proxy server of address: https://proxy-server-address:proxy-server-port 
                        
    2) Create a netCDF (.nc) file of the data called `woof_nam_gph_500.nc` saved at Weather_Data/WOOF-NAM/NETCDF.
    
    Linux Shell:
        ```wxdata-woof-nam fetch latest -v geopotential_height -l 500 \
            --netcdf True --ncdir Weather_Data/WOOF-NAM/NETCDF --ncfname woof_nam_gph_500.nc \ 
            --proxy https://proxy-server-address:proxy-server-port```
            
    Windows Powershell:
        ```wxdata-woof-nam fetch latest -v geopotential_height -l 500 `
            --netcdf True --ncdir Weather_Data/WOOF-NAM/NETCDF --ncfname woof_nam_gph_500.nc ` 
            --proxy https://proxy-server-address:proxy-server-port```
    
    """
@woof_nam.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=84,
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
        
@_click.option('--variables', 
              '-v', 
              default=['geopotential_height',
                        'temperature',
                        'relative_humidity',
                        'vertical_velocity_pressure',
                        'vertical_velocity_height',
                        'u-component_of_wind',
                        'v-component_of_wind',
                        'turbulent_kinetic_energy'],
              multiple=True, 
              type=str,
              help=(
                  """Variables to pass into the function. 
                  
                  Default=['geopotential height',
                        'temperature',
                        'relative humidity',
                        'vertical velocity (pressure)',
                        'vertical velocity (height)',
                        'u-component of wind',
                        'v-component of wind',
                        'turbulent kinetic energy']
                  
                  See https://edrewitz.github.io/WxData/WOOF-NAM%20CLI for available variables."""
                  
                  )
)

@_click.option(
    '--levels', 
    '-l', 
    default=['1000',
            '925',
            '850',
            '700',
            '500',
            '300',
            '250',
            '100',
            '50'],
    multiple=True, 
    type=str,  
    help=("""Levels for pressure in hPa. 
          
          Default=[1000,
                     925,
                     850,
                     700,
                     500,
                     300,
                     250,
                     100,
                     50]
          
          See https://edrewitz.github.io/WxData/WOOF-NAM%20CLI for available levels.
          
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
          
          See https://edrewitz.github.io/WxData/WOOF-NAM%20CLI for available level types.
          
          """)
)

@_click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://proxy-server-address:proxy-server-port). Default: no proxy.",
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
    default=f"WOOF-NAM/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"woof_nam.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)
def get_woof_nam(final_forecast_hour,
                 clear_recycle_bin,
                 custom_directory,
                 clear_data,
                 convert_temperature,
                 convert_to,
                 variables,
                 levels,
                 level_type,
                 proxy,
                 process,
                 netcdf,
                 ncdir,
                 ncfname):
    
    """Downloads Latest WOOF-NAM Data"""
    
    try:
        if custom_directory.lower() == "none":
            custom_directory = f"WOOF-NAM"
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
            if v == 'vertical velocity height':
                v = 'vertical velocity (height)'
            if v == 'vertical velocity pressure':
                v = 'vertical velocity (pressure)'
            if v == 'mslp eta reduction':
                v = 'mslp (eta model reduction)'
            if v == 'liquid volumetric soil moisture non-frozen':
                v = 'liquid volumetric soil moisture (non-frozen)'
            if v == 'parcel lifted index':
                v = 'parcel lifted index (to 500mb)'
            vars_fixed.append(v)
            
        convert_to = convert_to.lower()
        level_type = level_type.replace('_', ' ')
        if level_type == 'height_above_ground_layer_helicity':
            level_type = 'height above ground layer (helicity)'
        elif level_type == 'height_above_ground_layer_shear':
            level_type = 'height above ground layer (shear)'
        else:
            level_type = level_type
        
        _fetch_woof_nam(final_forecast_hour=final_forecast_hour,
                        path=custom_directory,
                        proxies=proxy,
                        clear_data=clear_data,
                        clear_recycle_bin=clear_recycle_bin,
                        convert_temperature=convert_temperature,
                        convert_to=convert_to,
                        process_data=process,
                        level_type=level_type,
                        variables=vars_fixed,
                        levels=levels,
                        to_netcdf=netcdf,
                        netcdf_path=ncdir,
                        netcdf_filename=ncfname,
                        return_values=False)
        if custom_directory != "none" and custom_directory != None:
            _click.echo(f"WOOF-NAM latest download complete, data files saved to {custom_directory}")
        else:
            if current_os != "Windows":
                _click.echo(f"WOOF-NAM latest download complete, data files saved to WOOF-NAM/ ")
            else:
                _click.echo(rf"WOOF-NAM latest download complete, data files saved to WOOF-NAM\ ")
            
    except SystemExit as e:
        _command_error_message('woof-nam')
        _sys.exit(1)
        

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    woof_nam_data()
    
if __name__ == "__main__":
    main()
