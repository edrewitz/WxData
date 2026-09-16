import click
import sys

from wxdata.model_data.noaa.gfs.gfs import(
    gfs_0p25 as _fetch_gfs_0p25,
    gfs_0p25_secondary_parameters as _fetch_gfs_0p25_secondary_parameters,
    gfs_0p50 as _fetch_gfs_0p50
)

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Please run `gfs {model.lower()} -h to view the help documentation.")
    print(f"Please visit: https://github.com/edrewitz/WxData/wiki#global-forecast-system-gfs for full detailed documentation.")

def _parse_proxy(value):
    if value is None:
        return None

    # Accept either http://host:port or https://host:port
    return {
        "http": value,
        "https": value,
    }

# ---------------------------------------------------------------------
# Top-level CLI group
# ---------------------------------------------------------------------
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def gfs_data():
    """RTMA command line utilities."""
    pass

# ---------------------------------------------------------------------
# GFS 0.25x0.25 Commands
# ---------------------------------------------------------------------
@gfs_data.group()
def gfs0p25():
    """
    GFS 0.25x0.25 Client.
    
    Valid Commands
    
    --------------
    
    -c = Category (Default=primary).
    
    This determines the category of variables and levels.
    
    -f = Final Forecast Hour (Default=384).
     
    The last hour the user wishes to download in the dataset. GFS0P25 has 384 forecast hours.
    
    -s = Source (Default=noaa). 
    
    Selects the primary data server to use.
    If the primary server is unavailable the client will rotate and try other servers.
    
    Server Choices
    
    -------------
    
    noaa - NCEP/NOMADS
    
    aws - Amazon Web Services
    
    google - Google Cloud Servers
    
    -cd = Clear Data (Default=False).
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data. 
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.
    The default path is f:GFS0P25/ATMOSPHERIC. 
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -v = Variables(Default=['geopotential_height', 'temperature', 'relative_humidity', 'u-component_of_wind', 'v-component_of_wind']) 
                       
    The list of variables the user wants to query.
    
    Here is a sample of how to query geopotential height and temperature `model gfs0p25 fetch -v geopotential_height -v temperature`
    
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
    
    -l = Levels (Default=[1000, 925, 850, 700, 500, 400, 300, 250, 200, 100, 50, 10])
                            
    Here is a sample of how to query geopotential height and temperature at 850 and 500mb `model gfs0p25 latest -v geopotential_height -v temperature -l 850 -l 500`
    
    The default setting of levels assume pressure levels are being used.
    
    -lt = Level Type (Default=pressure).
    
    This corresponds to the type of level.
    
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
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    Example: `model gfs0p25 latest -v geopotential height -l 500 --proxy https://proxy-server-address:proxy-server-port`
    
    """
    
@gfs0p25.command("latest")
@click.option(
    "--category",
    "-c",
    default="primary",
    type=str,
    show_default=True,
    help=(""""This determines whether the user downloads primary or secondary data variables
          
          Default=primary
          
          set -c secondary for secondary variables.
          
          """
    )
)

@click.option(
    "--final_forecast_hour",
    "-f",
    default=384,
    type=int,
    show_default=True,
    help="This is the final forecast hour requested in the dataset."
)

@click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
    show_default=True,
)

@click.option(
    "--clear_recycle_bin",
    "-cr",
    default=False,
    show_default=True,
    help="To clear your recycle bin with each run of the script set to True."
)

@click.option(
    "--custom_directory",
    "-cdir",
    default=None,
    show_default=True,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@click.option(
    "--clear_data",
    "-cd",
    default=False,
    show_default=True,
    help="To bypass the safety scanner set --clear data to False."
)

@click.option(
    "--source",
    "-s",
    default="noaa",
    show_default=True,
    help="Default noaa is for NCEP/NOMADS - set to aws to switch to Amazon Web Services or google to switch to Google Cloud"
)
        
@click.option('--variables', 
              '-v', 
              default=['geopotential_height',
                       'temperature',
                       'relative_humidity',
                       'u-component_of_wind'
                       'v-component_of_wind'],
              multiple=True, 
              help=(
                  """"Variables to pass into the function. 
                  
                  Default=['geopotential_height',
                            'temperature',
                            'relative_humidity',
                            'u-component_of_wind'
                            'v-component_of_wind']
                  
                  See https://edrewitz.github.io/WxData/GFS0P25 for available variables."""
                  
                  )
)

@click.option(
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
          
          Default=[1000,
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
                    10]
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available levels.
          
          """)
)

@click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          See https://edrewitz.github.io/WxData/GFS0P25 for available level types.
          
          """)
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
                  category):
    
    """Downloads Latest GFS 0.25x0.25 Data (Primary Variables)"""
    
    try:
        vars_fixed = []
        for v in variables:
            v = v.replace('_', ' ')
            vars_fixed.append(v)
            
        level_type = level_type.replace('_', ' ')
        
        category = category.lower()
        
        if category == 'primary':
        
            _fetch_gfs_0p25(final_forecast_hour=final_forecast_hour,
                            process_data=False,
                            proxies=proxy,
                            clear_recycle_bin=clear_recycle_bin,
                            custom_directory=custom_directory,
                            clear_data=clear_data,
                            source=source,
                            variables=vars_fixed,
                            levels=levels,
                            level_type=level_type)
            
        else:
            
            _fetch_gfs_0p25_secondary_parameters(final_forecast_hour=final_forecast_hour,
                            process_data=False,
                            proxies=proxy,
                            clear_recycle_bin=clear_recycle_bin,
                            custom_directory=custom_directory,
                            clear_data=clear_data,
                            source=source,
                            variables=vars_fixed,
                            levels=levels,
                            level_type=level_type)
        
        if custom_directory == True:
            click.echo(f"GFS0P25 {category.upper()} latest download complete, data files saved to {custom_directory}")
        else:
            click.echo(f"GFS0P25 {category.upper()} latest download complete, data files saved to GFS0P25/ATMOSPHERIC")
            
    except SystemExit as e:
        _command_error_message('gfs0p25')
        sys.exit(1)

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    gfs_data()
    
if __name__ == "__main__":
    main()