"""
This file hosts the functions responsible for GEFS data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025-2026
"""
import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import(
    file_paths_for_xarray as _file_paths_for_xarray,
    clear_gefs_idx_files as _clear_gefs_idx_files
)

from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import(
    shift_longitude as _shift_longitude,
    convert_lon as _convert_lon
)

_eccodes_warning()
_sys.tracebacklimit = 0
_logging.disable()

def primary_gefs_post_processing(paths,
                                 western_bound,
                                 eastern_bound,
                                 southern_bound,
                                 northern_bound):
    
    """
    This function post-processes the GEFS (Primary) Parameters for GEFS0P50 and GEFS0P25. 
    
    Required Arguments: 
    
    1) paths (List) - A list of file paths to the GEFS0P50 or GEFS0P25 files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Returns
    -------
    
    An xarray data array of the post-processed GEFS data. 
    GRIB Keys are converted to Plain Language Keys. 
    
    New Variable Keys After Post-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
    GEFS0P50
    --------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'convective_available_potential_energy'
    'convective_inhibition'
    'geopotential_height'
    'air_temperature'
    'relative_humidity'
    'u_wind_component'
    'v_wind_component'
    
    GEFS0P25
    --------
    
    'surface_pressure'
    'total_precipitation'
    'categorical_snow'
    'categorical_ice_pellets'
    'categorical_freezing_rain'
    'categorical_rain'
    'time_mean_surface_latent_heat_flux'
    'time_mean_surface_sensible_heat_flux'
    'surface_downward_shortwave_radiation_flux'
    'surface_downward_longwave_radiation_flux'
    'surface_upward_shortwave_radiation_flux'
    'surface_upward_longwave_radiation_flux'
    'orography'
    'water_equivalent_of_accumulated_snow_depth'
    'snow_depth'
    'sea_ice_thickness'
    'surface_visibility'
    'surface_wind_gust'
    'percent_frozen_precipitation'
    'convective_available_potential_energy'
    'convective_inhibition'
    'mslp'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_temperature'
    '2m_relative_humidity'
    '2m_dew_point'
    'maximum_temperature'
    'minimum_temperature'
    '10m_u_wind_component'
    '10m_v_wind_component'
    'precipitable_water'
    'mixed_layer_cape'
    'mixed_layer_cin'
    '3km_helicity'
    
    """
    
    # Returns an Error if pip was unable to install eccodes - This is an issue in latest versions of Python (>= 3.14)
    _eccodes_error_message()
    
    western_bound, eastern_bound = _convert_lon(western_bound, 
                                                    eastern_bound) 

    _clear_gefs_idx_files(paths)

    if len(paths) > 1:
        
        paths = _file_paths_for_xarray(paths)
        try:
            ds_list_1 = []
            
            for path in paths:
                file_pattern = path
                ds1 = _xr.open_mfdataset(file_pattern, 
                                        concat_dim='step', 
                                        combine='nested', 
                                        coords='minimal', 
                                        engine='cfgrib', 
                                        compat='override', 
                                        decode_timedelta=False,
                                        backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                    latitude=slice(northern_bound, southern_bound, 1))
                ds1 = _shift_longitude(ds1)
                ds_list_1.append(ds1)
        except Exception as e:
            pass             

        try:
            ds = _xr.concat(ds_list_1, 
                           dim='number')
        except Exception as e:
            pass                
        
    else:
        
        file_pattern = _file_paths_for_xarray(paths)
        
        try:
            ds = _xr.open_mfdataset(file_pattern, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                    latitude=slice(northern_bound, southern_bound, 1))
            ds = _shift_longitude(ds)
        except Exception as e:
            pass
        
    try: 
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass    
    
    try: 
        ds['total_precipitation'] = ds['tp']
        ds = ds.drop_vars('tp')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_snow'] = ds['csnow']
        ds = ds.drop_vars('csnow')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_ice_pellets'] = ds['cicep']
        ds = ds.drop_vars('cicep')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_freezing_rain'] = ds['cfrzr']
        ds = ds.drop_vars('cfrzr')
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_rain'] = ds['crain']
        ds = ds.drop_vars('crain')
    except Exception as e:
        pass  
    
    try:     
        ds['time_mean_surface_latent_heat_flux'] = ds['avg_slhtf']
        ds = ds.drop_vars('avg_slhtf')
    except Exception as e:
        pass  
      
    try:     
        ds['time_mean_surface_sensible_heat_flux'] = ds['avg_ishf']
        ds = ds.drop_vars('avg_ishf')
    except Exception as e:
        pass   
    
    try:     
        ds['surface_downward_shortwave_radiation_flux'] = ds['sdswrf']
        ds = ds.drop_vars('sdswrf')
    except Exception as e:
        pass    
    
    try:     
        ds['surface_downward_longwave_radiation_flux'] = ds['sdlwrf']
        ds = ds.drop_vars('sdlwrf')
    except Exception as e:
        pass    
    
    try:     
        ds['surface_upward_shortwave_radiation_flux'] = ds['suswrf']
        ds = ds.drop_vars('suswrf')
    except Exception as e:
        pass    
    
    try:     
        ds['surface_upward_longwave_radiation_flux'] = ds['sulwrf']
        ds = ds.drop_vars('sulwrf')
    except Exception as e:
        pass    

    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass
    
    try:     
        ds['water_equivalent_of_accumulated_snow_depth'] = ds['sdwe']
        ds = ds.drop_vars('sdwe')
    except Exception as e:
        pass   
    
    try:     
        ds['snow_depth'] = ds['sde']
        ds = ds.drop_vars('sde')
    except Exception as e:
        pass    
    
    try:     
        ds['sea_ice_thickness'] = ds['sithick']
        ds = ds.drop_vars('sithick')
    except Exception as e:
        pass     
    
    try:        
        ds['surface_visibility'] = ds['vis']
        ds = ds.drop_vars('vis')
    except Exception as e:
        pass       
    
    try:        
        ds['surface_wind_gust'] = ds['gust']
        ds = ds.drop_vars('gust')
    except Exception as e:
        pass   
    
    try:        
        ds['percent_frozen_precipitation'] = ds['cpofp']
        ds = ds.drop_vars('cpofp')
    except Exception as e:
        pass        
    
    try:     
        ds['mslp'] = ds['prmsl']
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass           
    try:        
        ds['soil_temperature'] = ds['st']
        ds = ds.drop_vars('st')
    except Exception as e:
        pass
       
    try:        
        ds['volumetric_soil_moisture_content'] = ds['soilw']
        ds = ds.drop_vars('soilw')
    except Exception as e:
        pass
    
    try:     
        ds['2m_temperature'] = ds['t2m']
        ds = ds.drop_vars('t2m')
    except Exception as e:
        pass 
    
    try:
        ds['2m_relative_humidity'] = ds['r2']
        ds = ds.drop_vars('r2')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds['d2m']
        ds = ds.drop_vars('d2m')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
    except Exception as e:
        pass
    
    try:
        ds['maximum_temperature'] = ds['tmax']
        ds = ds.drop_vars('tmax')
    except Exception as e:
        pass
    
    try:
        ds['minimum_temperature'] = ds['tmin']
        ds = ds.drop_vars('tmin')
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds['u10']
        ds = ds.drop_vars('u10')
    except Exception as e:
        pass

    try:
        ds['10m_v_wind_component'] = ds['v10']
        ds = ds.drop_vars('v10')
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds['pwat']
        ds = ds.drop_vars('pwat')
    except Exception as e:
        pass
    
    try:
        ds['convective_available_potential_energy'] = ds['cape']
        ds = ds.drop_vars('cape')
    except Exception as e:
        pass
    
    try:
        ds['convective_inhibition'] = ds['cin']
        ds = ds.drop_vars('cin')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass
    
    try:
        ds['temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    try:
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds['u']
        ds = ds.drop_vars('u')
    except Exception as e:
        pass

    try:
        ds['v_wind_component'] = ds['v']
        ds = ds.drop_vars('v')
    except Exception as e:
        pass
    
    try:
        ds['3km_helicity'] = ds['hlcy']
        ds = ds.drop_vars('hlcy')
    except Exception as e:
        pass
    
    _clear_gefs_idx_files(paths)
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        pass
    
    return ds


def secondary_gefs_post_processing(paths,
                                   western_bound,
                                   eastern_bound,
                                   southern_bound,
                                   northern_bound):
    
    
    """
    This function post-processes the GEFS (Secondary) Parameters for GEFS0P50 and GEFS0P25. 
    
    Required Arguments: 
    
    1) 1) paths (List) - A list of file paths to the GEFS0P50 Secondary Parameters. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Returns
    -------
    
    An xarray data array of the post-processed GEFS data. 
    GRIB Keys are converted to Plain Language Keys. 
    
    New Variable Keys After Post-Processing (Decrypted GRIB Keys Into Plain Language)
    --------------------------------------------------------------------------------
    
    'temperature'
    'surface_visibility'
    'surface_wind_gust'
    'haines_index'
    'plant_canopy_surface_water'
    'snow_cover'
    'percent_frozen_precipitation'
    'snow_phase_change_heat_flux'
    'surface_roughness'
    'frictional_velocity'
    'wilting_point'
    'field_capacity'
    'sunshine_duration'
    'surface_lifted_index'
    'best_4_layer_lifted_index'
    'land_sea_mask'
    'sea_ice_area_fraction'
    'orography'
    'convective_precipitation_rate'
    'precipitation_rate'
    'total_convective_precipitation'
    'total_non_convective_precipitation'
    'total_precipitation'
    'water_runoff'
    'ground_heat_flux'
    'time_mean_u_component_of_atmospheric_surface_momentum_flux'
    'time_mean_v_component_of_atmospheric_surface_momentum_flux'
    'instantaneous_eastward_gravity_wave_surface_flux'
    'instantaneous_northward_gravity_wave_surface_flux'
    'uv_b_downward_solar_flux'
    'clear_sky_uv_b_downward_solar_flux'
    'average_surface_albedo'
    'mslp'
    'mslp_eta_reduction'  
    'ventilation_rate'
    'geopotential_height'
    'vertical_velocity'
    'u_wind_component'
    'v_wind_component'
    'ozone_mixing_ratio'
    'absolute_vorticity'
    'cloud_mixing_ratio'
    'icing_severity'
    'total_cloud_cover'
    'relative_humidity'
    'liquid_volumetric_soil_moisture_non_frozen'
    'soil_temperature'
    'volumetric_soil_moisture_content'
    '2m_specific_humidity'
    '2m_dew_point'
    '2m_apparent_temperature'
    'specific_humidity'
    'pressure'
    'cloud_water'
    'total_ozone'
    'brightness_temperature'
    '3km_helicity'
    'u_component_of_storm_motion'
    'v_component_of_storm_motion'
    'pressure'
    'tropopause_standard_atmosphere_reference_height'
    '995_sigma_theta'
    'potential_vorticity'
    'vertical_speed_shear'
    'theta_level_montgomery_potential'
    'potential_vorticity_level_vertical_speed_shear'
    'mixed_layer_dew_point'
    'mixed_layer_precipitable_water'
    'parcel_lifted_index_to_500hPa'
    'convective_available_potential_energy'
    'convective_inhibition'
    'pressure_level_from_which_a_parcel_was_lifted'
    
    """
    
    # Returns an Error if pip was unable to install eccodes - This is an issue in latest versions of Python (>= 3.14)
    _eccodes_error_message()

    western_bound, eastern_bound = _convert_lon(western_bound, 
                                                    eastern_bound) 
            
    _clear_gefs_idx_files(paths)

    if len(paths) == 1:
        
        file_pattern = _file_paths_for_xarray(paths)
        
        try:
            ds = _xr.open_mfdataset(file_pattern, 
                                   concat_dim='step', 
                                   combine='nested', 
                                   coords='minimal', 
                                   engine='cfgrib', 
                                   compat='override',
                                   decode_timedelta=False,
                                    backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                    latitude=slice(northern_bound, southern_bound, 1))
            ds = _shift_longitude(ds)
        except Exception as e:
            pass    
        
    else:
        
        _clear_gefs_idx_files(paths)

        paths = _file_paths_for_xarray(paths)
        try:
            ds_list_1 = []      
            for path in paths:
                file_pattern = path
                ds = _xr.open_mfdataset(file_pattern, 
                                       concat_dim='step',
                                       combine='nested',
                                       coords='minimal', 
                                       engine='cfgrib', 
                                       compat='override', 
                                       decode_timedelta=False,
                                    backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                    latitude=slice(northern_bound, southern_bound, 1))
                ds = _shift_longitude(ds)
                ds_list_1.append(ds)
        except Exception as e:
            pass           
    
        try:    
            ds = _xr.concat(ds_list_1,
                           dim='number')
        except Exception as e:
            pass                       
        
    try:
        ds['temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    try:        
        ds['surface_visibility'] = ds['vis']
        ds = ds.drop_vars('vis')
    except Exception as e:
        pass        
    try:        
        ds['surface_wind_gust'] = ds['gust']
        ds = ds.drop_vars('gust')
    except Exception as e:
        pass        
    try:        
        ds['haines_index'] = ds['hindex']
        ds = ds.drop_vars('hindex')
    except Exception as e:
        pass        
    try:        
        ds['plant_canopy_surface_water'] = ds['cnwat']
        ds = ds.drop_vars('cnwat')
    except Exception as e:
        pass        
    try:        
        ds['snow_cover'] = ds['snowc']
        ds = ds.drop_vars('snowc')
    except Exception as e:
        pass        
    try:        
        ds['percent_frozen_precipitation'] = ds['cpofp']
        ds = ds.drop_vars('cpofp')
    except Exception as e:
        pass        
    try:        
        ds['snow_phase_change_heat_flux'] = ds['snohf']
        ds = ds.drop_vars('snohf')
    except Exception as e:
        pass        
    try:        
        ds['surface_roughness'] = ds['fsr']
        ds = ds.drop_vars('fsr')
    except Exception as e:
        pass        
    try:        
        ds['frictional_velocity'] = ds['fricv']
        ds = ds.drop_vars('fricv')
    except Exception as e:
        pass        
    try:        
        ds['wilting_point'] = ds['wilt']
        ds = ds.drop_vars('wilt')
    except Exception as e:
        pass        
    try:        
        ds['field_capacity'] = ds['fldcp']
        ds = ds.drop_vars('fldcp')
    except Exception as e:
        pass        
    try:        
        ds['sunshine_duration'] = ds['SUNSD']
        ds = ds.drop_vars('SUNSD')
    except Exception as e:
        pass        
    try:        
        ds['surface_lifted_index'] = ds['lftx']
        ds = ds.drop_vars('lftx')
    except Exception as e:
        pass        
    try:        
        ds['best_4_layer_lifted_index'] = ds['lftx4']
        ds = ds.drop_vars('lftx4')
    except Exception as e:
        pass        
    try:        
        ds['land_sea_mask'] = ds['lsm']
        ds = ds.drop_vars('lsm')
    except Exception as e:
        pass        
    try:        
        ds['sea_ice_area_fraction'] = ds['siconc']
        ds = ds.drop_vars('siconc')
    except Exception as e:
        pass        
    try:        
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass        
        
    try:        
        ds['convective_precipitation_rate'] = ds['cpr']
        ds = ds.drop_vars('cpr')
    except Exception as e:
        pass        
    try:        
        ds['precipitation_rate'] = ds['prate']
        ds = ds.drop_vars('prate')
    except Exception as e:
        pass        
    try:        
        ds['total_convective_precipitation'] = ds['acpcp']
        ds = ds.drop_vars('acpcp')
    except Exception as e:
        pass        
    try:        
        ds['total_non_convective_precipitation'] = ds['ncpcp']
        ds = ds.drop_vars('ncpcp')
    except Exception as e:
        pass        
    try:        
        ds['total_precipitation'] = ds['total_convective_precipitation'] + ds['total_non_convective_precipitation']
    except Exception as e:
        pass        
    try:        
        ds['water_runoff'] = ds['watr']
        ds = ds.drop_vars('watr')
    except Exception as e:
        pass        
    try:        
        ds['ground_heat_flux'] = ds['gflux']
        ds = ds.drop_vars('gflux')
    except Exception as e:
        pass        
    try:        
        ds['time_mean_u_component_of_atmospheric_surface_momentum_flux'] = ds['avg_utaua']
        ds = ds.drop_vars('avg_utaua')
    except Exception as e:
        pass        
    try:        
        ds['time_mean_v_component_of_atmospheric_surface_momentum_flux'] = ds['avg_vtaua']
        ds = ds.drop_vars('avg_vtaua')
    except Exception as e:
        pass        
    try:        
        ds['instantaneous_eastward_gravity_wave_surface_flux'] = ds['iegwss']
        ds = ds.drop_vars('iegwss')
    except Exception as e:
        pass        
    try:        
        ds['instantaneous_northward_gravity_wave_surface_flux'] = ds['ingwss']
        ds = ds.drop_vars('ingwss')
    except Exception as e:
        pass        
    try:        
        ds['uv_b_downward_solar_flux'] = ds['duvb']
        ds = ds.drop_vars('duvb')
    except Exception as e:
        pass        
    try:        
        ds['clear_sky_uv_b_downward_solar_flux'] = ds['cduvb']
        ds = ds.drop_vars('cduvb')
    except Exception as e:
        pass        
    try:        
        ds['average_surface_albedo'] = ds['avg_al']
        ds = ds.drop_vars('avg_al')
    except Exception as e:
        pass        
    try:        
        ds['mslp'] = ds['msl']
        ds = ds.drop_vars('msl')
    except Exception as e:
        pass        
    try:        
        ds['mslp_eta_reduction'] = ds['mslet']  
        ds = ds.drop_vars('mslet')
    except Exception as e:
        pass              
    try:        
        ds['ventilation_rate'] = ds['VRATE']   
        ds = ds.drop_vars('VRATE')
    except Exception as e:
        pass        
    try:        
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass        
      
    try:        
        ds['vertical_velocity'] = ds['w']
        ds = ds.drop_vars('w')
    except Exception as e:
        pass        
    try:        
        ds['u_wind_component'] = ds['u']
        ds = ds.drop_vars('u')
    except Exception as e:
        pass        
    try:        
        ds['v_wind_component'] = ds['v'] 
        ds = ds.drop_vars('v')
    except Exception as e:
        pass        
    try:        
        ds['ozone_mixing_ratio'] = ds['o3mr']
        ds = ds.drop_vars('o3mr')
    except Exception as e:
        pass        
    try:        
        ds['absolute_vorticity'] = ds['absv']
        ds = ds.drop_vars('absv')
    except Exception as e:
        pass        
    try:        
        ds['cloud_mixing_ratio'] = ds['clwmr']
        ds = ds.drop_vars('clwmr')
    except Exception as e:
        pass        
    try:        
        ds['icing_severity'] = ds['ICSEV']
        ds = ds.drop_vars('ICSEV')
    except Exception as e:
        pass        
    try:        
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('tcc')
    except Exception as e:
        pass        
    try:        
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass        
    try:        
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds['soill']
        ds = ds.drop_vars('soill')
    except Exception as e:
        pass        
    try:        
        ds['soil_temperature'] = ds['st']
        ds = ds.drop_vars('st')
    except Exception as e:
        pass        
    try:        
        ds['volumetric_soil_moisture_content'] = ds['soilw']
        ds = ds.drop_vars('soilw')
    except Exception as e:
        pass        
    try:        
        ds['2m_specific_humidity'] = ds['sh2']
        ds = ds.drop_vars('sh2')
    except Exception as e:
        pass        
    
    try:        
        ds['2m_dew_point'] = ds['d2m']
        ds = ds.drop_vars('d2m')
    except Exception as e:
        pass        
    try:        
        ds['2m_apparent_temperature'] = ds['aptmp']
        ds = ds.drop_vars('aptmp')
    except Exception as e:
        pass        
    try:        
        ds['specific_humidity'] = ds['q']
        ds = ds.drop_vars('q')
    except Exception as e:
        pass          
    try:        
        ds['pressure'] = ds['pres']
        ds = ds.drop_vars('pres')
    except Exception as e:
        pass             
   
    try:        
        ds['cloud_water'] = ds['cwat']
        ds = ds.drop_vars('cwat')
    except Exception as e:
        pass        
    try:        
        ds['total_ozone'] = ds['tozne']
        ds = ds.drop_vars('tozne')
    except Exception as e:
        pass        
   
    try:        
        ds['brightness_temperature'] = ds['btmp']
        ds = ds.drop_vars('btmp')
    except Exception as e:
        pass        
    try:        
        ds['3km_helicity'] = ds['hlcy']
        ds = ds.drop_vars('hlcy') 
    except Exception as e:
        pass        
    try:        
        ds['u_component_of_storm_motion'] = ds['ustm']
        ds = ds.drop_vars('ustm')
    except Exception as e:
        pass        
    try:        
        ds['v_component_of_storm_motion'] = ds['vstm']
        ds = ds.drop_vars('vstm')
    except Exception as e:
        pass        
    
    try:        
        ds['tropopause_pressure'] = ds['trpp']
        ds = ds.drop_vars('trpp')
    except Exception as e:
        pass        
    try:        
        ds['tropopause_standard_atmosphere_reference_height'] = ds['icaht']
        ds = ds.drop_vars('icaht')
    except Exception as e:
        pass        
                       
    try:        
        ds['vertical_speed_shear'] = ds['vwsh']
        ds = ds.drop_vars('vwsh')
    except Exception as e:
        pass                           
                          
    try:        
        ds['995_sigma_theta'] = ds['pt']
        ds = ds.drop_vars('pt')
    except Exception as e:
        pass              
               
    try:        
        ds['potential_vorticity'] = ds['pv']
        ds = ds.drop_vars('pv')
    except Exception as e:
        pass                          
          
    try:        
        ds['theta_level_montgomery_potential'] = ds['mont']
        ds = ds.drop_vars('mont')
    except Exception as e:
        pass                           
              
    try:        
        ds['mixed_layer_dew_point'] = ds['dpt']
        ds = ds.drop_vars('dpt')
    except Exception as e:
        pass        
    try:        
        ds['mixed_layer_precipitable_water'] = ds['pwat']
        ds = ds.drop_vars('pwat')
    except Exception as e:
        pass        
    try:        
        ds['parcel_lifted_index_to_500hPa'] = ds['pli']
        ds = ds.drop_vars('pli')
    except Exception as e:
        pass        
    try:        
        ds['convective_available_potential_energy'] = ds['cape']
        ds = ds.drop_vars('cape')
    except Exception as e:
        pass        
    try:        
        ds['convective_inhibition'] = ds['cin']
        ds = ds.drop_vars('cin')
    except Exception as e:
        pass        
    try:        
        ds['pressure_level_from_which_a_parcel_was_lifted'] = ds['plpl']
        ds = ds.drop_vars('plpl')
    except Exception as e:
        pass   

    try:
        ds = ds.drop_vars('unknown')
    except Exception as e:
        pass

    _clear_gefs_idx_files(paths)
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        pass

    return ds

