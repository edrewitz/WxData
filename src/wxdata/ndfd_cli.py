"""
This file hosts the WxData Command Line Interface for retrieving the National Weather Service NDFD Gridded Forecast

Command Line Use: `wxdata-ndfd **args`

(C) Eric J. Drewitz 2025-2026
"""

import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.gridded_forecasts.noaa.nws import get_ndfd_grids as _get_ndfd_grids

def _invalid_variable(variable):
    
    """Error Message for invalid variable"""
    
    print(f"Error: User entered an invalid variable of {variable}")
    print(f"""
          
          ***Valid Variables***
          
            maximum_relative_humidity
            mainimum_relative_humidity
            maximum_temperature
            minimum_temperature
            relative_humidity
            temperature
            apparent_temperature
            wind_speed
            wind_gust
            wind_direction
            spc_critical_fire_weather_forecast
            spc_dry_lightning_forecast
            spc_convective_outlook
            ice_accumulation
            probability_of_hail
            12_hour_probability_of_precipitation
            probability_of_extreme_tornadoes
            total_probability_of_severe_thunderstorms
            total_probability_of_extreme_severe_thunderstorms
            probability_of_extreme_thunderstorm_winds
            probability_of_extreme_hail
            probability_of_extreme_tornadoes
            probability_of_damaging_thunderstorm_winds
            quantitative_precipitation_forecast
            sky_cover
            snow_amount
            snow_level
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental
            dew_point
            visibility
            significant_wave_height
            warnings
            weather       
          
          """)

def _command_error_message(parameter):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Please run `wxdata-ndfd -h to view the help documentation.")
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
def ndfd_data():
    """NDFD command line utilities."""
    pass

# ---------------------------------------------------------------------
# ECMWF IFS Commands
# ---------------------------------------------------------------------
@ndfd_data.group(name='fetch')
def ndfd():
    """_summary_
    """
    
@ndfd.command("latest")
@_click.option(
    "--variable",
    "-v",
    type=str,
    help=("""Select the variable you would like to download.
          
          ***Variables***
          
            maximum_relative_humidity
            mainimum_relative_humidity
            maximum_temperature
            minimum_temperature
            relative_humidity
            temperature
            apparent_temperature
            wind_speed
            wind_gust
            wind_direction
            spc_critical_fire_weather_forecast
            spc_dry_lightning_forecast
            spc_convective_outlook
            ice_accumulation
            probability_of_hail
            12_hour_probability_of_precipitation
            probability_of_extreme_tornadoes
            total_probability_of_severe_thunderstorms
            total_probability_of_extreme_severe_thunderstorms
            probability_of_extreme_thunderstorm_winds
            probability_of_extreme_hail
            probability_of_extreme_tornadoes
            probability_of_damaging_thunderstorm_winds
            quantitative_precipitation_forecast
            sky_cover
            snow_amount
            snow_level
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_cumulative
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_34kts_incremental
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_cumulative
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_50kts_incremental
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_cumulative
            probabilistic_tropical_cyclone_surface_wind_speeds_greater_than_64kts_incremental
            dew_point
            visibility
            significant_wave_height
            warnings
            weather       
          
          """
    )
)

@_click.option(
    "--region",
    "-r",
    default="conus",
    show_default=True,
    type=str,
    help=("""This is the region the data is in.
          
          Use the 2-letter state identifier or use conus for CONUS.
          
          Defaults to CONUS.
          
          """
    )
)

@_click.option(
    "--source",
    "-s",
    default="noaa",
    show_default=True,
    type=str,
    help="Default noaa is for NOAA/NWS/FTP - set to aws to switch to Amazon Web Services"
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
    "--include_extended_grids",
    "-e",
    default=True,
    show_default=True,
    type=bool,
    help=("""Set to True to include the grids for the extended forecast. (Default=True)
          
          Set to False for SPC Outlooks where there are no external forecast grids. 
          
          """)
           
)

@_click.option(
    "--notifications",
    "-n",
    default="on",
    show_default=True,
    type=str,
    help=("""Set to "on" to recieve notifications about your download. (Default="on")
          
          To turn off set -n off
          
          """)
           
)

@_click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)

def fetch_ndfd_grids(variable,
                     region,
                     source,
                     clear_recycle_bin,
                     include_extended_grids,
                     proxy,
                     notifications):
    
    try:
        try:
            variable = variable.lower()
        except Exception as e:
            _invalid_variable(variable)
            _sys.exit(1)
            
        region = region.lower()
        source = source.lower()
        _get_ndfd_grids(variable,
                        region,
                        proxies=proxy,
                        clear_recycle_bin=clear_recycle_bin,
                        include_extended_grids=include_extended_grids,
                        source=source,
                        notifications=notifications)
    except Exception as e:
        _command_error_message(variable)
        _sys.exit(1)
        
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    ndfd_data()
    
if __name__ == "__main__":
    main()