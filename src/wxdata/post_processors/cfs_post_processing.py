"""
This file hosts the function responsible for CFS data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025-2026
"""

import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import sorted_paths as _sorted_paths
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import shift_longitude as _shift_longitude

_sys.tracebacklimit = 0
_logging.disable()

def cfs_flux_post_processing(path):
    
    """
    This function post-processes all GRIB2 Keys into a Plain Language Format for CFS Flux Data.
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array of CFS Flux Data with variable keys decoded into plain-language.
    
    CFS Flux Data Variables In Plain-Language Format
    ------------------------------------------------
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
    
    files = _sorted_paths(path)
    
    try:
        ds = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'depthBelowLandLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds = _shift_longitude(ds)
    except Exception as e:
        pass
    
    try:
        ds1 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'depthBelowLandLayer', 'paramId':3086}, 
                                backend_kwargs={"indexpath": ""})
        
        ds1 = _shift_longitude(ds1)
    except Exception as e:
        pass
    
    try:
        ds2 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'surface'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds2 = _shift_longitude(ds2)
    except Exception as e:
        pass
    
    try:
        ds3 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'nominalTop'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds3 = _shift_longitude(ds3)
    except Exception as e:
        pass
    
    try:
        ds4 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'highCloudLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds4 = _shift_longitude(ds4)
    except Exception as e:
        pass
    
    try:
        ds5 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'highCloudTop'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds5 = _shift_longitude(ds5)
    except Exception as e:
        pass
    
    try:
        ds6 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'highCloudBottom'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds6 = _shift_longitude(ds6)
    except Exception as e:
        pass
    
    try:
        ds7 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'middleCloudLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds7 = _shift_longitude(ds7)
    except Exception as e:
        pass
    
    try:
        ds8 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'middleCloudTop'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds8 = _shift_longitude(ds8)
    except Exception as e:
        pass
    
    try:
        ds9 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'middleCloudBottom'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds9 = _shift_longitude(ds9)
    except Exception as e:
        pass
    
    try:
        ds10 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'lowCloudLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds10 = _shift_longitude(ds10)
    except Exception as e:
        pass
    
    try:
        ds11 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'lowCloudTop'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds11 = _shift_longitude(ds11)
    except Exception as e:
        pass
    
    try:
        ds12 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'lowCloudBottom'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds12 = _shift_longitude(ds12)
    except Exception as e:
        pass
    
    try:
        ds13 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds13 = _shift_longitude(ds13)
    except Exception as e:
        pass
    
    try:
        ds14 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':167}, 
                                backend_kwargs={"indexpath": ""})
        
        ds14 = _shift_longitude(ds14)
    except Exception as e:
        pass
    
    try:
        ds15 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':174096}, 
                                backend_kwargs={"indexpath": ""})
        
        ds15 = _shift_longitude(ds15)
    except Exception as e:
        pass
    
    try:
        ds16 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':3015}, 
                                backend_kwargs={"indexpath": ""})
        
        ds16 = _shift_longitude(ds16)
    except Exception as e:
        pass
    
    try:
        ds17 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':3016}, 
                                backend_kwargs={"indexpath": ""})
        
        ds17 = _shift_longitude(ds17)
    except Exception as e:
        pass
    
    try:
        ds18 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':260282}, 
                                backend_kwargs={"indexpath": ""})
        
        ds18 = _shift_longitude(ds18)
    except Exception as e:
        pass
    
    try:
        ds19 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':260283}, 
                                backend_kwargs={"indexpath": ""})
        
        ds19 = _shift_longitude(ds19)
    except Exception as e:
        pass
    
    try:
        ds20 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds20 = _shift_longitude(ds20)
    except Exception as e:
        pass
    
    try:
        ds21 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'convectiveCloudLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds21 = _shift_longitude(ds21)
    except Exception as e:
        pass
    
    try:
        ds22 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'boundaryLayerCloudLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds22 = _shift_longitude(ds22)
    except Exception as e:
        pass
    
    try:
        ds23 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'hybrid'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds23 = _shift_longitude(ds23)
    except Exception as e:
        pass
    
    
    try:        
        ds['volumetric_soil_moisture_content'] = ds['soilw']
        ds = ds.drop_vars('soilw')
    except Exception as e:
        pass
    
    try:
        ds['soil_temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    
    try:        
        ds['liquid_volumetric_soil_moisture_non_frozen'] = ds['soill']
        ds = ds.drop_vars('soill')
    except Exception as e:
        pass  
    
    try:
        ds['soil_moisture_content'] = ds1['ssw']
    except Exception as e:
        pass
    
    try:
        ds['u_component_atmospheric_surface_momentum_flux'] = ds2['utaua']
    except Exception as e:
        pass
    
    try:
        ds['v_component_atmospheric_surface_momentum_flux'] = ds2['vtaua']
    except Exception as e:
        pass
    
    try:
        ds['instantaneous_surface_sensible_heat_net_flux'] = ds2['ishf']
    except Exception as e:
        pass
    
    try:
        ds['surface_latent_heat_net_flux'] = ds2['slhtf']
    except Exception as e:
        pass
    
    try:
        ds['surface_temperature'] = ds2['t']
    except Exception as e:
        pass
    
    try:
        ds['water_equivalent_of_accumulated_snow_depth'] = ds2['sdwe']
    except Exception as e:
        pass
    
    try:
        ds['surface_downward_longwave_radiation_flux'] = ds2['sdlwrf']
    except Exception as e:
        pass
    
    try:
        ds['surface_upward_longwave_radiation_flux'] = ds2['sulwrf']
    except Exception as e:
        pass
    
    try:
        ds['surface_upward_shortwave_radiation_flux'] = ds2['suswrf']
    except Exception as e:
        pass
    
    try:
        ds['surface_downward_shortwave_radiation_flux'] = ds2['sdswrf']
    except Exception as e:
        pass
    
    try:        
        ds['clear_sky_uv_b_downward_solar_flux'] = ds2['cduvb']
    except Exception as e:
        pass 
    
    try:        
        ds['precipitation_rate'] = ds2['prate']
    except Exception as e:
        pass   
    
    try:        
        ds['convective_precipitation_rate'] = ds2['cpr']
    except Exception as e:
        pass    
    
    try:        
        ds['ground_heat_flux'] = ds2['gflux']
    except Exception as e:
        pass  
    
    try:        
        ds['land_sea_mask'] = ds2['lsm']
    except Exception as e:
        pass   
        
    try:        
        ds['sea_ice_area_fraction'] = ds2['siconc']
    except Exception as e:
        pass     
    
    try: 
        ds['surface_pressure'] = ds2['sp']
    except Exception as e:
        pass  
    
    try:        
        ds['water_runoff'] = ds2['watr']
    except Exception as e:
        pass   
    
    try:        
        ds['instantaneous_eastward_gravity_wave_surface_flux'] = ds2['iegwss']
    except Exception as e:
        pass        
    
    try:        
        ds['instantaneous_northward_gravity_wave_surface_flux'] = ds2['ingwss']
    except Exception as e:
        pass 
    
    try:
        ds['surface_albedo'] - ds2['al']
    except Exception as e:
        pass
    
    try:     
        ds['sea_ice_thickness'] = ds2['sithick']
    except Exception as e:
        pass    
    
    try:     
        ds['snow_depth'] = ds2['sde']
    except Exception as e:
        pass  
    
    try:        
        ds['plant_canopy_surface_water'] = ds2['cnwat']
    except Exception as e:
        pass   
    
    try:        
        ds['surface_roughness'] = ds2['fsr']
    except Exception as e:
        pass   
    
    try:
        ds['vegetation'] = ds2['veg']
    except Exception as e:
        pass
    
    try:
        ds['vegetation_type'] = ds['vgtyp']
    except Exception as e:
        pass
    
    try:
        ds['soil_type'] = ds2['slt']
    except Exception as e:
        pass
    
    try:
        ds['surface_slope_type'] = ds2['sltyp']
    except Exception as e:
        pass
    
    try:        
        ds['frictional_velocity'] = ds2['fricv']
    except Exception as e:
        pass    
    
    try:
        ds['orography'] = ds2['orog']
    except Exception as e:
        pass
    
    try: 
        ds['categorical_rain'] = ds2['crain']
    except Exception as e:
        pass 
    
    try:
        ds['exchange_coefficient'] = ds2['sfexc']
    except Exception as e:
        pass
    
    try:
        ds['aerodynamic_conductance'] = ds2['acond']
    except Exception as e:
        pass
    
    try:
        ds['storm_surface_runoff'] = ds2['ssrun']
    except Exception as e:
        pass
    
    try:
        ds['direct_evaporation_from_bare_soil'] = ds2['evbs']
    except Exception as e:
        pass
    
    try:
        ds['canopy_water_evaporation'] = ds2['evcw']
    except Exception as e:
        pass
    
    try:
        ds['transpiration'] = ds2['trans']
    except Exception as e:
        pass
    
    try:
        ds['sublimation'] = ds2['sbsno']
    except Exception as e:
        pass
    
    try:
        ds['snow_cover'] = ds2['snowc']
    except Exception as e:
        pass
    
    try:
        ds['clear_sky_downward_longwave_flux'] = ds2['csdlf']
    except Exception as e:
        pass
    
    try:
        ds['clear_sky_upward_solar_flux'] = ds2['csusf']
    except Exception as e:
        pass
    
    try:
        ds['clear_sky_downward_solar_flux'] = ds2['csdsf']
    except Exception as e:
        pass
    
    try:
        ds['clear_sky_upward_longwave_flux'] = ds2['csulf']
    except Exception as e:
        pass
    
    try:
        ds['snow_phase_change_heat_flux'] = ds2['snohf']
    except Exception as e:
        pass
    
    try:
        ds['visible_beam_downward_solar_flux'] = ds2['vbdsf']
    except Exception as e:
        pass
    
    try:
        ds['near_ir_beam_downward_solar_flux'] = ds2['nbdsf']
    except Exception as e:
        pass
    
    try:
        ds['near_ir_diffuse_downward_solar_flux'] = ds2['nddsf']
    except Exception as e:
        pass
    
    try:
        ds['snowfall_rate_water_equivalent'] = ds2['srweq']
    except Exception as e:
        pass
    
    try:
        ds['nominal_top_of_the_atmosphere_upward_longwave_radiation_flux'] = ds3['sulwrf']
    except Exception as e:
        pass
    
    try:
        ds['nominal_top_of_the_atmosphere_upward_shortwave_radiation_flux'] = ds3['suswrf']
    except Exception as e:
        pass
    
    try:
        ds['nominal_top_of_the_atmosphere_downward_shortwave_radiation_flux'] = ds3['sdswrf']
    except Exception as e:
        pass
    
    try:
        ds['nominal_top_of_the_atmosphere_clear_sky_upward_longwave_radiation_flux'] = ds3['csulf']
    except Exception as e:
        pass
    
    try:
        ds['nominal_top_of_the_atmosphere_clear_sky_upward_solar_flux'] = ds3['csusf']
    except Exception as e:
        pass
    
    try:        
        ds['total_high_cloud_cover'] = ds4['tcc']
    except Exception as e:
        pass   
    
    try:
        ds['high_cloud_top_level_pressure'] = ds5['pres']
    except Exception as e:
        pass
    
    try:
        ds['high_cloud_top_level_temperature'] = ds5['t']
    except Exception as e:
        pass
    
    try:
        ds['high_cloud_bottom_pressure'] = ds6['pres']
    except Exception as e:
        pass
    
    try:
        ds['total_middle_cloud_cover'] = ds7['tcc']
    except Exception as e:
        pass
    
    try:
        ds['middle_cloud_top_level_pressure'] = ds8['pres']
    except Exception as e:
        pass
    
    try:
        ds['middle_cloud_top_level_temperature'] = ds8['t']
    except Exception as e:
        pass
    
    try:
        ds['middle_cloud_bottom_pressure'] = ds9['pres']
    except Exception as e:
        pass
    
    try:
        ds['total_low_cloud_cover'] = ds10['tcc']
    except Exception as e:
        pass
    
    try:
        ds['low_cloud_top_level_pressure'] = ds11['pres']
    except Exception as e:
        pass
    
    try:
        ds['low_cloud_top_level_temperature'] = ds11['t']
    except Exception as e:
        pass
    
    try:
        ds['low_cloud_bottom_pressure'] = ds12['pres']
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds13['u10']
    except Exception as e:
        pass

    try:
        ds['10m_v_wind_component'] = ds13['v10']
    except Exception as e:
        pass
    
    try:     
        ds['2m_temperature'] = ds14['t2m']
    except Exception as e:
        pass 
    
    try:        
        ds['2m_specific_humidity'] = ds15['sh2']
    except Exception as e:
        pass  
    
    try:
        ds['maximum_temperature'] = ds16['tmax']
    except Exception as e:
        pass
    
    try:
        ds['minimum_temperature'] = ds17['tmin']
    except Exception as e:
        pass
    
    try:
        ds['maximum_specific_humidity'] = ds18['qmax']
    except Exception as e:
        pass
    
    try:
        ds['minimum_specific_humidity'] = ds19['qmin']
    except Exception as e:
        pass
    
    try:
        ds['cloud_work_function'] = ds20['cwork']
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds20['pwat']
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds20['tcc']
    except Exception as e:
        pass
    
    try:
        ds['total_convective_cloud_cover'] = ds21['tcc']
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover_boundary_layer'] = ds22['tcc']
    except Exception as e:
        pass
    
    try:
        ds['995_sigma_temperature'] = ds23['t']
    except Exception as e:
        pass
    
    try:
        ds['995_sigma_specific_humidity'] = ds23['q']
    except Exception as e:
        pass
    
    try:
        ds['995_sigma_u_wind_component'] = ds23['u']
    except Exception as e:
        pass
    
    try:
        ds['995_sigma_v_wind_component'] = ds23['v']
    except Exception as e:
        pass
    
    try:
        ds['995_sigma_geopotential_height'] = ds23['gh']
    except Exception as e:
        pass
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message()
        _sys.exit(1)
    
    return ds



def cfs_pressure_post_processing(path):
    
    """
    This function post-processes all GRIB2 Keys into a Plain Language Format for CFS Pressure Data.
    
    Required Arguments:
    
    1) path (String) - The path to the files.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray.array of CFS Pressure Data with variable keys decoded into plain-language.
    
    CFS Pressure Data Variables In Plain-Language Format
    ----------------------------------------------------
    
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
    
    files = _sorted_paths(path)
    
    try:
        ds = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'meanSea'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds = _shift_longitude(ds)
    except Exception as e:
        pass
    
    try:
        ds1 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds1 = _shift_longitude(ds1)
    except Exception as e:
        pass
    
    try:
        ds2 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':260080}, 
                                backend_kwargs={"indexpath": ""})
        
        ds2 = _shift_longitude(ds2)
    except Exception as e:
        pass
    
    try:
        ds3 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':3027}, 
                                backend_kwargs={"indexpath": ""})
        
        ds3 = _shift_longitude(ds3)
    except Exception as e:
        pass
    
    try:
        ds4 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':260084}, 
                                backend_kwargs={"indexpath": ""})
        
        ds4 = _shift_longitude(ds4)
    except Exception as e:
        pass
    
    try:
        ds5 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGround'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds5 = _shift_longitude(ds5)
    except Exception as e:
        pass
    
    try:
        ds6 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'surface'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds6 = _shift_longitude(ds6)
    except Exception as e:
        pass
    
    try:
        ds7 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'atmosphereSingleLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds7 = _shift_longitude(ds7)
    except Exception as e:
        pass
    
    try:
        ds8 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds8 = _shift_longitude(ds8)
    except Exception as e:
        pass
    
    try:
        ds9 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'paramId':260070}, 
                                backend_kwargs={"indexpath": ""})
        
        ds9 = _shift_longitude(ds9)
    except Exception as e:
        pass
    
    try:
        ds10 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveGroundLayer', 'paramId':260071}, 
                                backend_kwargs={"indexpath": ""})
        
        ds10 = _shift_longitude(ds10)
    except Exception as e:
        pass
    
    try:
        ds11 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'tropopause'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds11 = _shift_longitude(ds11)
    except Exception as e:
        pass
    
    try:
        ds12 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'maxWind'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds12 = _shift_longitude(ds12)
    except Exception as e:
        pass
    
    try:
        ds13 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'heightAboveSea'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds13 = _shift_longitude(ds13)
    except Exception as e:
        pass
    
    try:
        ds14 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'isothermZero'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds14 = _shift_longitude(ds14)
    except Exception as e:
        pass
    
    try:
        ds15 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'highestTroposphericFreezing'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds15 = _shift_longitude(ds15)
    except Exception as e:
        pass
    
    try:
        ds16 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds16 = _shift_longitude(ds16)
    except Exception as e:
        pass
    
    try:
        ds17 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'paramId': 59}, 
                                backend_kwargs={"indexpath": ""})
        
        ds17 = _shift_longitude(ds17)
    except Exception as e:
        pass
    
    try:
        ds18 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'pressureFromGroundLayer', 'paramId': 228001}, 
                                backend_kwargs={"indexpath": ""})
        
        ds18 = _shift_longitude(ds18)
    except Exception as e:
        pass
    
    try:
        ds19 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'sigmaLayer'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds19 = _shift_longitude(ds19)
    except Exception as e:
        pass
    
    try:
        ds20 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'sigma'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds20 = _shift_longitude(ds20)
    except Exception as e:
        pass
    
    try:
        ds21 = _xr.open_mfdataset(files,
                                 concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                filter_by_keys={'typeOfLevel': 'potentialVorticity'}, 
                                backend_kwargs={"indexpath": ""})
        
        ds21 = _shift_longitude(ds21)
    except Exception as e:
        pass
    
    
    try:
        ds['mslp'] = ds['msl']
        ds = ds.drop_vars('msl')
    except Exception as e:
        pass
    
    try:
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds1['gh']
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds1['t']
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds1['r']
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds1['q']
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds1['w']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds1['u']
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component'] = ds1['v']
    except Exception as e:
        pass
    
    try:
        ds['absolute_vorticity'] = ds1['absv']
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds1['o3mr']
    except Exception as e:
        pass
    
    try:
        ds['stream_function'] = ds1['strf']
    except Exception as e:
        pass
    
    try:
        ds['velocity_potential'] = ds1['vp']
    except Exception as e:
        pass
    
    try:
        ds['5_wave_geopotential_height'] = ds2['wavh5']
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height_anomaly'] = ds3['gpa']
    except Exception as e:
        pass
    
    try:
        ds['5_wave_geopotential_height_anomaly'] = ds4['wava5']
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds5['d2m']
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = ds5['r2']
    except Exception as e:
        pass
    
    try:
        ds['total_precipitation'] = ds6['tp']
    except Exception as e:
        pass
    
    try:
        ds['total_convective_precipitation'] = ds6['acpcp']
    except Exception as e:
        pass
    
    try:        
        ds['total_non_convective_precipitation'] = ds6['ncpcp']
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_snow'] = ds6['csnow']
    except Exception as e:
        pass  
    
    try:
        ds['categorical_ice_pellets'] = ds6['cicep']
    except Exception as e:
        pass
    
    try: 
        ds['categorical_freezing_rain'] = ds6['cfrzr']
    except Exception as e:
        pass  
    
    try: 
        ds['categorical_rain'] = ds6['crain']
    except Exception as e:
        pass 
    
    try:        
        ds['surface_lifted_index'] = ds6['lftx']
    except Exception as e:
        pass 
    
    try:        
        ds['best_4_layer_lifted_index'] = ds6['lftx4']
    except Exception as e:
        pass    
    
    try:        
        ds['surface_cape'] = ds6['cape']
    except Exception as e:
        pass    
        
    try:        
        ds['surface_cin'] = ds6['cin']
    except Exception as e:
        pass 
    
    try:
        ds['cloud_water'] = ds7['cwat']
    except Exception as e:
        pass
    
    try:
        ds['entire_atmosphere_relative_humidity'] = ds7['r']
    except Exception as e:
        pass
    
    try:
        ds['total_ozone'] = ds7['tozne']
    except Exception as e:
        pass
    
    try:
        ds['storm_relative_helicity'] = ds8['hlcy']
    except Exception as e:
        pass
    
    try:        
        ds['u_component_of_storm_motion'] = ds9['ustm']
    except Exception as e:
        pass     
       
    try:        
        ds['v_component_of_storm_motion'] = ds10['vstm']
    except Exception as e:
        pass    
    
    try:
        ds['tropopause_pressure'] = ds11['trpp']
    except Exception as e:
        pass
    
    try:
        ds['tropopause_height'] = ds11['gh']
    except Exception as e:
        pass
    
    try:        
        ds['tropopause_u_wind_component'] = ds11['u']
    except Exception as e:
        pass        
    
    try:        
        ds['tropopause_v_wind_component'] = ds11['v']
    except Exception as e:
        pass      
            
    try:        
        ds['tropopause_temperature'] = ds11['t']
    except Exception as e:
        pass    
              
    try:        
        ds['tropopause_vertical_speed_shear'] = ds11['vwsh']
    except Exception as e:
        pass  
    
    try:        
        ds['max_wind_u_component'] = ds12['u']
    except Exception as e:
        pass  
                
    try:        
        ds['max_wind_v_component'] = ds12['v']
    except Exception as e:
        pass   
    
    try:
        ds['max_wind_geopotential_height'] = ds12['gh']
    except Exception as e:
        pass
    
    try:
        ds['max_wind_pressure'] = ds12['pres']
    except Exception as e:
        pass
    
    try:
        ds['max_wind_temperature'] = ds12['t']
    except Exception as e:
        pass
    
    try:
        ds['temperature_height_above_sea'] = ds13['t']
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component_height_above_sea'] = ds13['u']
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component_height_above_sea'] = ds13['v']
    except Exception as e:
        pass
    
    try:        
        ds['zero_deg_c_isotherm_geopotential_height'] = ds14['gh']
    except Exception as e:
        pass       
           
    try:        
        ds['zero_deg_c_isotherm_relative_humidity'] = ds14['r']
    except Exception as e:
        pass 
    
    try:        
        ds['highest_tropospheric_freezing_level_geopotential_height'] = ds15['gh']
    except Exception as e:
        pass   
               
    try:        
        ds['highest_tropospheric_freezing_level_relative_humidity'] = ds15['r']
    except Exception as e:
        pass  
    
    try:
        ds['mixed_layer_temperature'] = ds16['t']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_relative_humidity'] = ds16['r']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_specific_humidity'] = ds16['q']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_u_wind_component'] = ds16['u']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_v_wind_component'] = ds16['v']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_dew_point'] = ds16['dpt']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_precipitable_water'] = ds16['pwat']
    except Exception as e:
        pass
    
    try:
        ds['parcel_lifted_index'] = ds16['pli']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cape'] = ds17['cape']
    except Exception as e:
        pass
    
    try:
        ds['mixed_layer_cin'] = ds18['cin']
    except Exception as e:
        pass
    
    try:
        ds['sigma_layer_relative_humidity'] = ds19['r']
    except Exception as e:
        pass
    
    try:        
        ds['995_sigma_temperature'] = ds20['t']
    except Exception as e:
        pass  
                
    try:        
        ds['995_sigma_theta'] = ds20['pt']
    except Exception as e:
        pass   
    
    try:        
        ds['995_sigma_relative_humdity'] = ds20['r']
    except Exception as e:
        pass       
    
    try:        
        ds['995_u_wind_component'] = ds20['u']
    except Exception as e:
        pass     
             
    try:        
        ds['995_v_wind_component'] = ds20['v']
    except Exception as e:
        pass    
              
    try:        
        ds['995_vertical_velocity'] = ds20['w']
    except Exception as e:
        pass 
    
    try:        
        ds['potential_vorticity_level_u_wind_component'] = ds21['u']
    except Exception as e:
        pass       
           
    try:        
        ds['potential_vorticity_level_v_wind_component'] = ds21['v']
    except Exception as e:
        pass            
      
    try:        
        ds['potential_vorticity_level_temperature'] = ds21['t']
    except Exception as e:
        pass        
            
    try:        
        ds['potential_vorticity_level_geopotential_height'] = ds21['gh']
    except Exception as e:
        pass      
      
    try:        
        ds['potential_vorticity_level_air_pressure'] = ds21['pres']
    except Exception as e:
        pass       
     
    try:        
        ds['potential_vorticity_level_vertical_speed_shear'] = ds21['vwsh']
    except Exception as e:
        pass    
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message()
        _sys.exit(1)
    
    return ds