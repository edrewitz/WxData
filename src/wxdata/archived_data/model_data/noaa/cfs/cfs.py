"""
This file hosts the client that retrieves the requested NOAA Climate Forecast System (CFS) Data from the Amazon Web Services Archive.

(C) Eric J. Drewitz 2025-2026
"""
import os as _os
import wxdata.client.client as _client
import wxdata.post_processors.cfs_post_processing as _cfs_post_processing
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.transforms import grib_to_netcdf as _grib_to_netcdf
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
from wxdata.archived_data.model_data.noaa.cfs.url_scanner import(
    cfs_flux_url_scanner as _cfs_flux_url_scanner,
    cfs_pressure_url_scanner as _cfs_pressure_url_scanner
)

_eccodes_warning()

def get_archived_cfs_flux(
             date,
             run,
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90,
             final_forecast_hour=720,
             proxies=None,
             path=f"CFS Flux/Archive",
             process_data=True,
             notifications='off',
             convert_temperature=True,
             chunk_size=8192,
             convert_to='celsius',
             level_type='height above ground',
             variable='temperature',
             levels=[2],
            to_netcdf=False,
            netcdf_path=f"CFS FLUX/NETCDF",
            netcdf_filename=f"cfs_flux.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
    
    """
    This function is the URL Scanner for the NOAA Climate System Flux Products (CFS Flux) Data Archive.
    
    Server - Amazon Web Services
    
    The function scans to ensure the data the user requests is available and provides error messages if data is not available.
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    2) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    3) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    4) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    5) final_forecast_hour (Integer) - Default=720 (30-Days). The last forecast timestep the user wishes to download.
        The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
        6 hourly data for several months, processing times may be long. Must be a multiple of 6. 

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                                 
    7) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    8) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    9) path (String) - Default="CFS/Flux/Archive". The path of the local directory where the files will be stored.
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    12) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    13) level_type (String) - Default='height above ground'. The type of vertical coordinates for the list of variables.
    
        ***Level Types***
        
        'surface'
        'height above ground'
        'height below ground'
        'entire atmosphere'
        'top of atmosphere'
        'high cloud top level'
        'middle cloud top level'
        'low cloud top level'
        'high cloud bottom level'
        'middle cloud bottom level'
        'low cloud bottom level'
        'convective cloud layer'
        'boundary layer cloud layer'
        'height above sea level'
        'hybrid'

                                
    14) variable (String) - Default='temperature'.
    
        The variable the user selects to download.
    
        ***Variable Name List for CFS Flux Data***
        
			'aerodynamic conductance'
            'albedo'
            'clear sky uv-b downward solar flux'
            'plant canopy surface water'
            'convective precipitation rate'
            'categorical rain'
            'clear sky downward longwave flux'
            'clear sky downward solar flux (surface)'
            'clear sky downward solar flux (top of the atmosphere)'
            'clear sky upward solar flux'
            'cloud work function'
            'downward longwave radiation flux'
            'downward shortwave radiation flux'
            'clear sky uv-b downward solar flux'
            'direct evaporation from bare soil'
            'canopy water evaporation'
            'surface friction velocity'
            'ground heat flux'
            'geopotential height'
            'planetary boundary layer height'
            'ice cover'
            'ice thickness'
            'land cover'
            'latent heat net flux'
            'near ir beam downward solar flux'
            'near ir diffuse downward solar flux'
            'potential evaporation rate'
            'precipitation rate'
            'pressure'
            'precipitable water'
            '2-meter maximum specific humidity'
            '2-meter minimum specific humidity'
            'sublimation (evaporation from snow)'
            'surface roughness'
            'sedimentation mass flux'
            'sensible heat net flux'
            'surface slope type'
            'snow depth'
            'snow phase-change heat flux'
            'snow cover'
            'liquid volumetric soil moisture (non-frozen)'
            'soil moisture content'
            'volumetric soil moisture content'
            'soil type'
            'specific humidity'
            'snowfall rate water equivalent'
            'storm surface runoff (non-infiltrating)'
            'total cloud cover'
            'maximum temperature'
            'minimum temperature'
            'temperature'
            'transpiration'
            'momentum flux (u-component)'
            'u-component of wind'
            'zonal flux of gravity wave stress'
            'upward longwave radiation flux'
            'upward shortwave radiation flux'
            'visible beam downward solar flux'
            'vegetation'
            'momentum flux (v-component)'
            'v-component of wind'
            'vegetation type'
            'meridional flux of gravity wave stress'
            'water runoff'
            'water equivalent of accumulated snow depth'
            
    15) levels (Integer List) - Default=[2].
    
    The units for the level in the atmosphere (i.e. levels=[2] -> 2-meters above ground)
    
    16) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    17) netcdf_path (String) - Default='CFS FLUX/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    18) netcdf_filename (String) - Default='cfs_flux.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    19) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    20) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
            
    **Returns**
    
    A post-processes xarray.array where the GRIB variable keys are decoded into a plain-language format.
    
    ***CFS Flux Data Variables In Plain-Language Format***
    
        'volumetric_soil_moisture_content'
        'soil_temperature'
        'liquid_volumetric_soil_moisture_non_frozen'
        'soil_moisture_content'
        'u_component_atmospheric_surface_momentum_flux'
        'v_component_atmospheric_surface_momentum_flux'
        'instantaneous_surface_sensible_heat_net_flux'
        'surface_latent_heat_net_flux'
        'surface_temperature'
        'water_equivalent_of_accumulated_snow_depth'
        'surface_downward_longwave_radiation_flux'
        'surface_upward_longwave_radiation_flux'
        'surface_upward_shortwave_radiation_flux'
        'surface_downward_shortwave_radiation_flux'
        'clear_sky_uv_b_downward_solar_flux'
        'precipitation_rate'
        'convective_precipitation_rate'
        'ground_heat_flux'
        'land_sea_mask'
        'sea_ice_area_fraction'
        'surface_pressure'
        'instantaneous_eastward_gravity_wave_surface_flux'
        'instantaneous_northward_gravity_wave_surface_flux'
        'surface_albedo'
        'sea_ice_thickness'
        'snow_depth'
        'plant_canopy_surface_water'
        'surface_roughness'
        'vegetation'
        'vegetation_type'
        'soil_type'
        'surface_slope_type'
        'frictional_velocity'
        'orography'
        'categorical_rain'
        'exchange_coefficient'
        'aerodynamic_conductance'
        'storm_surface_runoff'
        'direct_evaporation_from_bare_soil'
        'canopy_water_evaporation'
        'transpiration'
        'sublimation'
        'snow_cover'
        'clear_sky_downward_longwave_flux'
        'clear_sky_upward_solar_flux'
        'clear_sky_downward_solar_flux'
        'clear_sky_upward_longwave_flux'
        'snow_phase_change_heat_flux'
        'visible_beam_downward_solar_flux'
        'near_ir_beam_downward_solar_flux'
        'near_ir_diffuse_downward_solar_flux'
        'snowfall_rate_water_equivalent'
        'nominal_top_of_the_atmosphere_upward_longwave_radiation_flux'
        'nominal_top_of_the_atmosphere_upward_shortwave_radiation_flux'
        'nominal_top_of_the_atmosphere_downward_shortwave_radiation_flux'
        'nominal_top_of_the_atmosphere_clear_sky_upward_longwave_radiation_flux'
        'nominal_top_of_the_atmosphere_clear_sky_upward_solar_flux'
        'total_high_cloud_cover'
        'high_cloud_top_level_pressure'
        'high_cloud_top_level_temperature'
        'high_cloud_bottom_pressure'
        'total_middle_cloud_cover'
        'middle_cloud_top_level_pressure'
        'middle_cloud_top_level_temperature'
        'middle_cloud_bottom_pressure'
        'total_low_cloud_cover'
        'low_cloud_top_level_pressure'
        'low_cloud_top_level_temperature'
        'low_cloud_bottom_pressure'
        '10m_u_wind_component'
        '10m_v_wind_component'
        '2m_temperature'
        '2m_specific_humidity'
        'maximum_temperature'
        'minimum_temperature'
        'maximum_specific_humidity'
        'minimum_specific_humidity'
        'cloud_work_function'
        'precipitable_water'
        'total_cloud_cover'
        'total_convective_cloud_cover'
        'total_cloud_cover_boundary_layer'
        '995_sigma_temperature'
        '995_sigma_specific_humidity'
        '995_sigma_u_wind_component'
        '995_sigma_geopotential_height'   
                               
    """
    
    variables = [variable]
    path = f"{path}/{variable.upper()}"
    
    urls, files, idx_urls = _cfs_flux_url_scanner(date,
                                 run,
                                 final_forecast_hour,
                                 proxies)
    if run > 10:
        path = f"{path}/{date}/{run}z"
    else:
            path = f"{path}/{date}/0{run}z"
            
    try:
        for file in _os.listdir(path):
            _os.remove(f"{path}/{file}")
    except Exception as e:
        pass
    
    for u, f, i in zip(urls, files, idx_urls):
        _client.byte_range_request(u,
                      i,
                      variables,
                      levels,
                      level_type,
                      path,
                      f,
                      proxies=proxies,
                      chunk_size=chunk_size,
                      notifications=notifications)
        
    if process_data == True:
        print(f"CFS Flux Data Processing...")
        
        ds = _cfs_post_processing.cfs_post_processing(path,
                                                        western_bound,
                                                        eastern_bound,
                                                        northern_bound,
                                                        southern_bound,
                                                        variable)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"CFS Flux Data Processing Complete.")
        if to_netcdf == True:
            if delete_previous_netcdf_file == True:
                try:
                    _os.remove(f"{netcdf_path}/{netcdf_filename}")
                except Exception as e:
                    pass
            
            _grib_to_netcdf(ds,
                            netcdf_path,
                            netcdf_filename)
        else:
            pass
        
        if return_values == True:    
            return ds
        else:
            pass
    
    else:
        pass 
    
    
def get_archived_cfs_pressure(
             date,
             run,
             western_bound=-180, 
             eastern_bound=180, 
             northern_bound=90, 
             southern_bound=-90,
             final_forecast_hour=720,
             proxies=None,
             path=f"CFS Pressure/Archive",
             process_data=True,
             notifications='off',
             convert_temperature=True,
             chunk_size=8192,
             convert_to='celsius',
             level_type='pressure',
             variable='geopotential height',
             levels=[1000, 
                    925, 
                    850, 
                    700, 
                    500, 
                    300, 
                    250],
            to_netcdf=False,
            netcdf_path=f"CFS PRESSURE/NETCDF",
            netcdf_filename=f"cfs_pressure.nc",
            delete_previous_netcdf_file=True,
            return_values=True):
    
    """
    This function is the URL Scanner for the NOAA Climate System Pressure Products (CFS Flux) Data Archive.
    
    Server - Amazon Web Services
    
    The function scans to ensure the data the user requests is available and provides error messages if data is not available.
    
    Required Arguments:
    
    1) date (String or datetime) - The date of the model run.
    
    2) run (Integer) - The model runtime in UTC (0, 6, 12, 18).
    
    Optional Arguments:
    
    1) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    2) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    3) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    4) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.

    5) final_forecast_hour (Integer) - Default=720 (30-Days). The last forecast timestep the user wishes to download.
        The CFS outputs 6 hourly data for the span of several months. Note that if the user wishes to download
        6 hourly data for several months, processing times may be long. Must be a multiple of 6. 

    6) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                                 
    7) chunk_size (Integer) - Default=8192. The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    8) notifications (String) - Default='off'. Notification when a file is downloaded and saved to {path}
    
    9) path (String) - Default="CFS/Pressure/Archive". The path of the local directory where the files will be stored.
    
    10) process_data (Boolean) - Default=True. When set to True, WxData will preprocess the model data. If the user wishes to process the 
       data via their own external method, set process_data=False which means the data will be downloaded but not processed. 
       
    11) convert_temperature (Boolean) - Default=True. When set to True, the temperature related fields will be converted from Kelvin to
        either Celsius or Fahrenheit. When False, this data remains in Kelvin.
        
    12) convert_to (String) - Default='celsius'. When set to 'celsius' temperature related fields convert to Celsius.
        Set convert_to='fahrenheit' for Fahrenheit. 
        
    13) level_type (String) - Default='height above ground'. The type of vertical coordinates for the list of variables.
    
        ***Level Types***
        
        'pressure'
        'surface'
        'height above ground'
        'entire atmosphere'
        'mean sea level'
        'tropopause'
        'height above sea level'
        'isothermal'
        'highest tropospheric freezing level'
        'pressure above ground'
        'sigma layer'
        'sigma level'
        'potential vorticity surface'

                                
    14) variable (String) - Default='geopotential height'.
    
    The variable the user selects to download.
        
        ***Variable Name List for CFS Pressure Data***
        
            'best lifted index'
            '5 wave geopotential height anomaly'
            '5 wave geopotential height'
            'absolute vorticity'
            'convective precipitation'
            'total precipitation'
            'convective available potential energy'
            'categorical freezing rain'
            'categorical ice pellets'
            'convective inhibition'
            'cloud mixing ratio'
            'categorical rain'
            'categorical snow'
            'cloud water'
            'dew point'
            'geopotential height anomaly'
            'geopotential height'
            'storm relative helicity'
            'surface lifted index'
            'large scale non-convective precipitation'
            'ozone mixing ratio'
            'parcel lifted index (to 500mb)'
            'potential temperature'
            'pressure'
            'mean sea level pressure'
            'precipitable water'
            'relative humidity'
            'specific humidity'
            'stream function'
            'temperature'
            'total ozone'
            'u-component of wind'
            'u-component of storm motion'
            'v-component of wind'
            'velocity potential'
            'v-component of storm motion'
            'vertical velocity (pressure)'
            'vertical speed shear'
            
    15) levels (Integer List) - Default=[1000, 925, 850, 700, 500, 300, 250]
    
    Available Levels
    ----------------
    
        1000
        975
        925
        900
        875
        850
        825
        800
        775
        750
        700
        650
        600
        550
        500
        450
        400
        350
        300
        250
        225
        200
        175
        150
        125
        100
        70
        50
        30
        20
        10
        7
        5
        3
        2
        1
    
    16) to_netcdf (Boolean) - Default=False. When set to True, the xarray.array in GRIB2 format and will be written to a netCDF (.nc) file.
    
    17) netcdf_path (String) - Default='CFS PRESSURE/NETCDF'. The directory where the converted netCDF (.nc) file will be written to.
    
    18) netcdf_filename (String) - Default='cfs_pressure.nc'. The name of the netCDF (.nc) file. A good practice is to 
        name this netCDF file using the variable name. 
        
    19) delete_previous_netcdf_file (Boolean) - Default=True. When set to True the previous netCDF (.nc) will be deleted before writing a 
        new netCDF file. For users who want to archive all data set this to False. 
        
    20) return_values (Boolean) - Default=True. When set to True, an xarray.array is returned. Set to False to have no values returned. 
            
    **Returns**
    
    A post-processes xarray.array where the GRIB variable keys are decoded into a plain-language format.
    
    ***CFS Pressure Data Variables In Plain-Language Format***
    
            'mslp'
            'geopotential_height'
            'air_temperature'
            'relative_humidity'
            'specific_humidity'
            'vertical_velocity'
            'u_wind_component'
            'v_wind_component'
            'absolute_vorticity'
            'ozone_mixing_ratio'
            'stream_function'
            'velocity_potential'
            '5_wave_geopotential_height'
            'geopotential_height_anomaly'
            '5_wave_geopotential_height_anomaly'
            '2m_dew_point'
            '2m_relative_humidity'
            'total_precipitation'
            'total_convective_precipitation'
            'total_non_convective_precipitation'
            'categorical_snow'
            'categorical_ice_pellets'
            'categorical_freezing_rain'
            'categorical_rain'
            'surface_lifted_index'
            'best_4_layer_lifted_index'
            'surface_cape'
            'surface_cin'
            'cloud_water'
            'entire_atmosphere_relative_humidity'
            'total_ozone'
            'storm_relative_helicity'
            'u_component_of_storm_motion'
            'v_component_of_storm_motion'
            'tropopause_pressure'
            'tropopause_height'
            'tropopause_u_wind_component'
            'tropopause_v_wind_component'
            'tropopause_temperature'
            'tropopause_vertical_speed_shear'
            'max_wind_u_component'
            'max_wind_v_component'
            'max_wind_geopotential_height'
            'max_wind_pressure'
            'max_wind_temperature'
            'temperature_height_above_sea'
            'u_wind_component_height_above_sea'
            'v_wind_component_height_above_sea'
            'zero_deg_c_isotherm_geopotential_height'
            'zero_deg_c_isotherm_relative_humidity'
            'highest_tropospheric_freezing_level_geopotential_height'
            'highest_tropospheric_freezing_level_relative_humidity'
            'mixed_layer_temperature'
            'mixed_layer_relative_humidity'
            'mixed_layer_specific_humidity'
            'mixed_layer_u_wind_component'
            'mixed_layer_v_wind_component'
            'mixed_layer_dew_point'
            'mixed_layer_precipitable_water'
            'parcel_lifted_index'
            'mixed_layer_cape'
            'mixed_layer_cin'
            'sigma_layer_relative_humidity'
            '995_sigma_temperature'
            '995_sigma_theta'
            '995_sigma_relative_humdity'
            '995_u_wind_component'
            '995_v_wind_component'
            '995_vertical_velocity'
            'potential_vorticity_level_u_wind_component'
            'potential_vorticity_level_v_wind_component'
            'potential_vorticity_level_temperature'
            'potential_vorticity_level_geopotential_height'
            'potential_vorticity_level_air_pressure'
            'potential_vorticity_level_vertical_speed_shear'    
                               
    """
    
    variables = [variable]
    path = f"{path}/{variable.upper()}"
    
    urls, files, idx_urls = _cfs_pressure_url_scanner(date,
                                 run,
                                 final_forecast_hour,
                                 proxies)
    if run > 10:
        path = f"{path}/{date}/{run}z"
    else:
            path = f"{path}/{date}/0{run}z"
            
    try:
        for file in _os.listdir(path):
            _os.remove(f"{path}/{file}")
    except Exception as e:
        pass
    
    for u, f, i in zip(urls, files, idx_urls):
        _client.byte_range_request(u,
                      i,
                      variables,
                      levels,
                      level_type,
                      path,
                      f,
                      proxies=proxies,
                      chunk_size=chunk_size,
                      notifications=notifications)
        
    if process_data == True:
        print(f"CFS Pressure Data Processing...")
        
        ds = _cfs_post_processing.cfs_post_processing(path,
                                                        western_bound,
                                                        eastern_bound,
                                                        northern_bound,
                                                        southern_bound,
                                                        variable)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"CFS Pressure Data Processing Complete.")
        if to_netcdf == True:
            if delete_previous_netcdf_file == True:
                try:
                    _os.remove(f"{netcdf_path}/{netcdf_filename}")
                except Exception as e:
                    pass
            
            _grib_to_netcdf(ds,
                            netcdf_path,
                            netcdf_filename)
        else:
            pass
        
        if return_values == True:    
            return ds
        else:
            pass
    
    else:
        pass 
        
        
