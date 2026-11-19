"""
This file hosts the post-processing for the WOOF-NAM Data.

(C) Eric J. Drewitz 2025-2026
"""
import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.file_funcs import sorted_paths as _sorted_paths
from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import shift_longitude as _shift_longitude


_eccodes_warning()
_sys.tracebacklimit = 0
_logging.disable()

def woof_nam_post_processing(path,
                             level_type):
    
    """
    
    
    """
    _eccodes_error_message()
    
    files = _sorted_paths(path)
    
    try:
        ds = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            backend_kwargs={"indexpath": ""})
        
        ds = _shift_longitude(ds,
                            x_y_dims=True)
    except Exception as e:
        pass
   
    if level_type == 'pressure':
        try:
            ds1 = _xr.open_mfdataset(files, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':156})
            
            ds1 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['geopotential_height'] = ds1['gh']
            ds = ds.drop_vars('gh')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':130})
            
            ds2 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['air_temperature'] = ds2['t']
            ds = ds.drop_vars('t')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':157})
            
            ds3 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['relative_humidity'] = ds3['r']
            ds = ds.drop_vars('r')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':135})
            
            ds4 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['vertical_velocity_pressure'] = ds4['w']
            ds = ds.drop_vars('w')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':131})
            
            ds5 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['u_wind_component'] = ds5['u']
            ds = ds.drop_vars('u')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':132})
            
            ds6 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['v_wind_component'] = ds6['v']
            ds = ds.drop_vars('v')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':260155})
            
            ds7 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['turbulent_kinetic_energy'] = ds7['tke']
            ds = ds.drop_vars('tke')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'isobaricInhPa', 'paramId':3041})
            
            ds8 = _shift_longitude(ds,
                                x_y_dims=True)
            
            ds['absolute_vorticity'] = ds8['absv']
            ds = ds.drop_vars('absv')
        except Exception as e:
            pass
        
    elif level_type == 'height above ground':
        try:
            ds1 = _xr.open_mfdataset(files, 
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':167})
            
            ds1 = _shift_longitude(ds1,
                                x_y_dims=True)
            
            ds['2m_temperature'] = ds1['t2m']
            ds = ds.drop_vars('t2m')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':174096})
            
            ds2 = _shift_longitude(ds2,
                                x_y_dims=True)
            
            ds['2m_specific_humidity'] = ds2['sh2']
            ds = ds.drop_vars('sh2')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':168})
            
            ds3 = _shift_longitude(ds3,
                                x_y_dims=True)
            
            ds['2m_dew_point'] = ds3['d2m']
            ds = ds.drop_vars('d2m')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':260242})
            
            ds4 = _shift_longitude(ds4,
                                x_y_dims=True)
            
            ds['2m_relative_humidity'] = ds4['r2']
            ds = ds.drop_vars('r2')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':165})
            
            ds5 = _shift_longitude(ds5,
                                x_y_dims=True)
            
            ds['10m_u_wind_component'] = ds5['u10']
            ds = ds.drop_vars('u10')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':166})
            
            ds6 = _shift_longitude(ds6,
                                x_y_dims=True)
            
            ds['10m_v_wind_component'] = ds6['v10']
            ds = ds.drop_vars('v10')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':130})
            
            ds7 = _shift_longitude(ds7,
                                x_y_dims=True)
            
            ds['air_temperature'] = ds7['t']
            ds = ds.drop_vars('t')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':133})
            
            ds8 = _shift_longitude(ds8,
                                x_y_dims=True)
            
            ds['specific_humidity'] = ds8['q']
            ds = ds.drop_vars('q')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':54})
            
            ds9 = _shift_longitude(ds9,
                                x_y_dims=True)
            
            ds['pressure'] = ds9['pres']
            ds = ds.drop_vars('pres')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':131})
            
            ds10 = _shift_longitude(ds10,
                                x_y_dims=True)
            
            ds['u_wind_component'] = ds10['u']
            ds = ds.drop_vars('u')
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
                                backend_kwargs={"indexpath": ""},
                                filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':132})
            
            ds11 = _shift_longitude(ds11,
                                x_y_dims=True)
            
            ds['v_wind_component'] = ds11['v']
            ds = ds.drop_vars('v')
        except Exception as e:
            pass

    try:
        ds['vertical_velocity_height'] = ds['wz']
        ds = ds.drop_vars('wz')
    except Exception as e:
        pass
    
    try:     
        ds['mslp'] = ds['prmsl']
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass      
    
    try:        
        ds['mslp_eta_reduction'] = ds['mslet']  
        ds = ds.drop_vars('mslet')
    except Exception as e:
        pass  
    
    try:
        ds['derived_radar_reflectivity'] = ds['refd']
        ds = ds.drop_vars('refd')
    except Exception as e:
        pass
    
    try:
        ds['maximum_composite_reflectivity'] = ds['refc']
        ds = ds.drop_vars('refc')
    except Exception as e:
        pass
    
    try:
        ds['precipitable_water'] = ds['pwat']
        ds = ds.drop_vars('pwat')
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('tcc')
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
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass    
    
    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    
    try:        
        ds['plant_canopy_surface_water'] = ds['cnwat']
        ds = ds.drop_vars('cnwat')
    except Exception as e:
        pass        
    
    try:     
        ds['water_equivalent_of_accumulated_snow_depth'] = ds['sdwe']
        ds = ds.drop_vars('sdwe')
    except Exception as e:
        pass   
    
    try:        
        ds['snow_cover'] = ds['snowc']
        ds = ds.drop_vars('snowc')
    except Exception as e:
        pass     
    
    try:     
        ds['snow_depth'] = ds['sde']
        ds = ds.drop_vars('sde')
    except Exception as e:
        pass   
    
    try:
        ds['direct_evaporation_cease_soil_moisture'] = ds['smdry']
        ds = ds.drop_vars('smdry')
    except Exception as e:
        pass
    
    try:
        ds['soil_porosity'] = ds['poros']
        ds = ds.drop_vars('poros')
    except Exception as e:
        pass
    
    try: 
        ds['total_precipitation'] = ds['tp']
        ds = ds.drop_vars('tp')
    except Exception as e:
        pass  
    
    try:        
        ds['total_convective_precipitation'] = ds['acpcp']
        ds = ds.drop_vars('acpcp')
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
        ds['drag_coefficient'] = ds['cd']
        ds = ds.drop_vars('cd')
    except Exception as e:
        pass
    
    try:
        ds['vegetation'] = ds['veg']
        ds = ds.drop_vars('veg')
    except Exception as e:
        pass
    
    try:
        ds['vegetation_type'] = ds['vgtyp']
        ds = ds.drop_vars('vgtyp')
    except Exception as e:
        pass
    
    try:
        ds['soil_type'] = ds['slt']
        ds = ds.drop_vars('slt')
    except Exception as e:
        pass
    
    try:
        ds['number_of_soil_layers_in_root_zone'] = ds['rlyrs']
        ds = ds.drop_vars('rlyrs')
    except Exception as e:
        pass
    
    try:        
        ds['wilting_point'] = ds['wilt']
        ds = ds.drop_vars('wilt')
    except Exception as e:
        pass   
    
    try:
        ds['transpiration_stress_onset'] = ds['smref']
        ds = ds.drop_vars('smref')
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
        ds['surface_albedo'] = ds['al']
        ds = ds.drop_vars('al')
    except Exception as e:
        pass
    
    try:
        ds['instantaneous_surface_sensible_heat_net_flux'] = ds['ishf']
        ds = ds.drop('ishf')
    except Exception as e:
        pass
    
    try:
        ds['surface_latent_heat_net_flux'] = ds['slhtf']
        ds = ds.drop_vars('slhtf')
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
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
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
        ds['ventilation_rate'] = ds['VRATE']
        ds = ds.drop_vars('VRATE')
    except Exception as e:
        pass
    
    
    
    try:
        if level_type == 'surface':
            ds['planetary_boundary_layer_height'] = ds['unknown']
        elif level_type == 'entire atmosphere single layer':
            ds['radar_echo_top_height'] = ds['unknown']

        ds = ds.drop_vars('unknown')     
    except Exception as e:
        pass
    
       
    return ds