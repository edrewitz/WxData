"""
This file hosts the function responsible for ECMWF data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025-2026
"""
import xarray as _xr
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.calc.thermodynamics import relative_humidity as _relative_humidity
from wxdata.utils.file_funcs import(
    clear_idx_files_in_path as _clear_idx_files_in_path,
    sorted_paths as _sorted_paths
)

_sys.tracebacklimit = 0
_logging.disable()


def ecmwf_ifs_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):
    
    """
    This function does the following:
    
    1) Subsets the ECMWF IFS and IFS Ensemble model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF IFS or ECMWF IFS Ensemble files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF IFS/ECMWF IFS Ensemble Variable Keys 
    -------------------------------------------------------------
    
    'total_column_water'
    'total_column_vertically_integrated_water_vapor'
    'total_cloud_cover'
    'snowfall'
    'snow_depth'
    'snow_albedo'
    'land_sea_mask'
    'specific_humidity'
    'volumetric_soil_moisture_content'
    'sea_ice_thickness'
    'soil_temperature'
    'surface_longwave_radiation_downward'
    'surface_net_shortwave_solar_radiation'
    'surface_net_longwave_thermal_radiation'
    'top_net_longwave_thermal_radiation'
    '10m_max_wind_gust'
    'vertical_velocity'
    'relative_vorticity'
    'relative_humidity'
    'geopotential_height'
    'eastward_turbulent_surface_stress'
    'u_wind_component'
    'divergence'
    'northward_turbulent_surface_stress'
    'v_wind_component'
    'air_temperature'
    'water_runoff'
    'total_precipitation'
    'mslp'
    'eastward_surface_sea_water_velocity'
    'most_unstable_cape'
    'northward_surface_sea_water_velocity'
    'sea_surface_height'
    'standard_deviation_of_sub_gridscale_orography'
    'skin_temperature'
    'slope_of_sub_gridscale_orography'
    '10m_u_wind_component'
    'precipitation_type'
    '10m_v_wind_component'
    'total_precipitation_rate'
    'surface_shortwave_radiation_downward'
    'geopotential'
    'surface_pressure'
    '2m_temperature'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    'time_maximum_10m_wind_gust'
    '3_hr_maximum_2m_temperature'
    '3_hr_minimum_2m_temperature'

    """
    _clear_idx_files_in_path(path)
    
    files = _sorted_paths(path)
    
    ds0 = None
    ds1 = None
    ds2 = None
    ds3 = None
    ds4 = None
    
    try:
        ds0 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':49}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                        latitude=slice(northern_bound, southern_bound, 1))
    
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':228246}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                       latitude=slice(northern_bound, southern_bound, 1))
    
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':228247}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                       latitude=slice(northern_bound, southern_bound, 1))
        
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':168}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                    latitude=slice(northern_bound, southern_bound, 1))
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':167}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                    latitude=slice(northern_bound, southern_bound, 1))
    except Exception as e:
        pass
    
    try:
        ds = ds.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    try:
        ds1 = ds1.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    try:
        ds2 = ds2.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
        
    try:
        ds3 = ds3.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    try:
        ds4 = ds4.drop_duplicates(dim="step", keep="first")
    except Exception as e:
        pass
    
    ds0_list = []
    
    try:
        ds0['snow_density'] = ds0['rsn']
        ds0 = ds0.drop_vars('rsn')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['total_column_water'] = ds0['tcw']
        ds0 = ds0.drop_vars('tcw')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['total_cloud_cover'] = ds0['tcc']
        ds0 = ds0.drop_vars('tcc')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['snowfall'] = ds0['sf']
        ds0 = ds0.drop_vars('sf')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['snow_depth'] = ds0['sd']
        ds0 = ds0.drop_vars('sd')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['total_column_vertically_integrated_water_vapor'] = ds0['tcwv']
        ds0 = ds0.drop_vars('tcwv')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['snow_albedo'] = ds0['asn']
        ds0 = ds0.drop_vars('asn')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['land_sea_mask'] = ds0['lsm']
        ds0 = ds0.drop_vars('lsm')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['specific_humidity'] = ds0['q']
        ds0 = ds0.drop_vars('q')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['volumetric_soil_moisture_content'] = ds0['vsw']
        ds0 = ds0.drop_vars('vsw')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['precipitable_water'] = ds0['tcvw']
        ds0 = ds0.drop_vars('tcvw')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:     
        ds0['sea_ice_thickness'] = ds0['sithick']
        ds0 = ds0.drop_vars('sithick')
        ds0_list.append(ds0)
    except Exception as e:
        pass     
    
    try:
        ds0['soil_temperature'] = ds0['sot']
        ds0 = ds0.drop_vars('sot')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['surface_longwave_radiation_downward'] = ds0['strd']
        ds0 = ds0.drop_vars('strd')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['time_maximum_10m_wind_gust'] = ds0['fg10']
        ds0 = ds0.drop_vars('fg10')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['surface_net_shortwave_solar_radiation'] = ds0['ssr']
        ds0 = ds0.drop_vars('ssr')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['surface_net_longwave_thermal_radiation'] = ds0['str']
        ds0 = ds0.drop_vars('str')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['top_net_longwave_thermal_radiation'] = ds0['ttr']
        ds0 = ds0.drop_vars('ttr')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['10m_max_wind_gust'] = ds0['max_i10fg']
        ds0 = ds0.drop_vars('max_i10fg')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['vertical_velocity'] = ds0['w']
        ds0 = ds0.drop_vars('w')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['relative_vorticity'] = ds0['vo']
        ds0 = ds0.drop_vars('vo')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['relative_humidity'] = ds0['r']
        ds0 = ds0.drop_vars('r')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['geopotential_height'] = ds0['gh']
        ds0 = ds0.drop_vars('gh')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['eastward_turbulent_surface_stress'] = ds0['ewss']
        ds0 = ds0.drop_vars('ewss')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['u_wind_component'] = ds0['u']
        ds0 = ds0.drop('u')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['divergence'] = ds0['d']
        ds0 = ds0.drop_vars('d')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['northward_turbulent_surface_stress'] = ds0['nsss']
        ds0 = ds0.drop_vars('nsss')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['v_wind_component'] = ds0['v']
        ds0 = ds0.drop_vars('v')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['air_temperature'] = ds0['t']
        ds0 = ds0.drop_vars('t')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['water_runoff'] = ds0['ro']
        ds0 = ds0.drop_vars('ro')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['3_hr_maximum_2m_temperature'] = ds0['mx2t3']
        ds0 = ds0.drop_vars('mx2t3')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['3_hr_minimum_2m_temperature'] = ds0['mn2t3']
        ds0 = ds0.drop_vars('mn2t3')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['total_precipitation'] = ds0['tp']
        ds0 = ds0.drop_vars('tp')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['mslp'] = ds0['msl']
        ds0 = ds0.drop_vars('msl')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['eastward_surface_sea_water_velocity'] = ds0['sve']
        ds0 = ds0.drop_vars('sve')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['most_unstable_cape'] = ds0['mucape']
        ds0 = ds0.drop_vars('mucape')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['northward_surface_sea_water_velocity'] = ds0['svn']
        ds0 = ds0.drop_vars('svn')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['sea_surface_height'] = ds0['zos']
        ds0 = ds0.drop_vars('zos')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['standard_deviation_of_sub_gridscale_orography'] = ds0['sdor']
        ds0 = ds0.drop_vars('sdor')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['skin_temperature'] = ds0['skt']
        ds0 = ds0.drop_vars('skt')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['slope_of_sub_gridscale_orography'] = ds0['slor']
        ds0 = ds0.drop_vars('slor')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['10m_u_wind_component'] = ds0['u10']
        ds0 = ds0.drop_vars('u10')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['precipitation_type'] = ds0['ptype']
        ds0 = ds0.drop_vars('ptype')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['10m_v_wind_component'] = ds0['v10']
        ds0 = ds0.drop_vars('v10')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['total_precipitation_rate'] = ds0['tprate']
        ds0 = ds0.drop_vars('tprate')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['surface_shortwave_radiation_downward'] = ds0['ssrd']
        ds0 = ds0.drop_vars('ssrd')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['surface_geopotential_height'] = ds0['z']
        ds0 = ds0.drop_vars('z')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['surface_pressure'] = ds0['sp']
        ds0 = ds0.drop_vars('sp')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['2m_temperature'] = ds0['t2m']
        ds0 = ds0.drop_vars('t2m')
        ds0 = _xr.concat(ds0, ds5, dim='step')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds1['time_maximum_10m_wind_gust'] = ds1['fg10']
        ds1 = ds1.drop_vars('fg10')
    except Exception as e:
        pass
    
    try:
        ds2['100m_u_wind_component'] = ds2['u100']
        ds2 = ds2.drop_vars('u100')
    except Exception as e:
        pass
    
    try:
        ds3['100m_v_wind_component'] = ds3['v100']
        ds3 = ds3.drop_vars('v100')
    except Exception as e:
        pass
    
    try:
        ds4['2m_dew_point'] = ds4['d2m']
        ds4 = ds4.drop_vars('d2m')
    except Exception as e:
        pass
    
    try:
        ds0 = _xr.concat(ds0_list, dim="time")
        ds0 = ds0.isel(time=0)
    except Exception as e:
        pass
    
    try:
    
        surface_ds_list = [ds0, ds1, ds2, ds3, ds4]
        
        surface_ds = []
        for d in surface_ds_list:
            if d is not None:
                try:
                    d = d.isel(time=0)
                except Exception as e:
                    pass
                surface_ds.append(d)
            else:
                pass
            
            
        
        ds = _xr.concat(surface_ds, 
                        dim='time', 
                        coords='minimal',
                        compat='override')
    
        try:
            ds = ds.drop_vars('d2m')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('ssrd')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('tcwv')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('ptype')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('lsm')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('tprate')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('asn')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sithick')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('strd')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('ssr')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('str')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('ttr')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('ewss')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('nsss')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('ro')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('tp')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sd')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sf')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('msl')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sve')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('mucape')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('svn')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('zos')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sdor')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('tcc')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('t2m')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('z')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sp')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('fg10')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('u10')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('v10')    
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('vo')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('r')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('w')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('gh')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('u')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('d')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('v')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('t')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sot')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('vsw')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('u100')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('v100')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('mx2t3')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('mn2t3')
        except Exception as e:
            pass
        try:
            ds['2m_relative_humidity'] = _relative_humidity(ds['2m_temperature'],
                                                        ds['2m_dew_point'])
        except Exception as e:
            pass
        
        try:
            ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
        except Exception as e:
            pass
        
        ds = ds.isel(time=0)
        
        try:
            ds = ds.transpose("number", "step", "latitude", "longitude")
        except Exception as e:
            pass
        
    except Exception as e:
        pass
        
    _clear_idx_files_in_path(path)
    
    try:    
        ds = ds.sortby('step')
        return ds
    except Exception as e:
       _eccodes_error_message()
       _sys.exit(1)
   
    

def ecmwf_aifs_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):
    
    """
    This function does the following:
    
    1) Subsets the ECMWF AIFS model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF AIFS files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF AIFS Variable Keys 
    ---------------------------------------
    
    'volumetric_soil_moisture_content'
    'soil_temperature'
    'geopotential'
    'specific_humidity'
    'u_wind_component'
    'v_wind_component'
    'air_temperature'
    'vertical velocity'
    '100m_u_wind_component'
    '100m_v_wind_component'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_dew_point_depression'
    'water_runoff' 
    'surface_geopotential_height'
    'skin_temperature'
    'surface_pressure'
    'standard_deviation_of_sub_gridscale_orography'
    'slope_of_sub_gridscale_orography'
    'surface_shortwave_radiation_downward'
    'land_sea_mask'
    'surface_longwave_radiation_downward'
    'convective_precipitation'
    'snowfall_water_equivalent'
    'total_precipitation'
    'low_cloud_cover'
    'middle_cloud_cover'
    'high_cloud_cover'
    'total_column_water'
    'total_cloud_cover'
    'mslp'
        
    """
    _clear_idx_files_in_path(path)
    
    files = _sorted_paths(path)
    
    ds0 = None
    ds1 = None
    ds2 = None
    ds3 = None
    ds4 = None
    ds5 = None
    ds6 = None
    ds7 = None
    ds8 = None
    ds9 = None
    ds10 = None
    ds11 = None
    ds12 = None
    
    try:
        ds0 = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False,
                            filter_by_keys={'typeOfLevel': 'soilLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'isobaricInhPa'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10u'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'shortName':'10v'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':167}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'heightAboveGround', 'paramId':168}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'surface'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'lowCloudLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'mediumCloudLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'highCloudLayer'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'entireAtmosphere'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
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
                            filter_by_keys={'typeOfLevel': 'meanSea'}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
                            
    except Exception as e:
        pass
    
    
    ###############
    # Soil Levels #
    ###############
    
    ds0_list = []
    
    try:
        ds0['volumetric_soil_moisture_content'] = ds0['vsw']
        ds0 = ds0.drop_vars('vsw')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0['soil_temperature'] = ds0['sot']
        ds0 = ds0.drop_vars('sot')
        ds0_list.append(ds0)
    except Exception as e:
        pass
    
    try:
        ds0 = _xr.concat(ds0_list, dim="time")
        ds0 = ds0.isel(time=0)
    except Exception as e:
        pass
    
    ###################
    # Pressure Levels #
    ###################
    
    ds1_list = []
    
    try:
        ds1['geopotential'] = ds1['z']
        ds1 = ds1.drop_vars('z')
        ds1_list.append(ds1)
    except Exception as e:
        pass
    
    try:
        ds1['specific_humidity'] = ds1['q']
        ds1 = ds1.drop_vars('q')
        ds1_list.append(ds1)
    except Exception as e:
        pass
    
    try:
        ds1['u_wind_component'] = ds1['u']
        ds1 = ds1.drop_vars('u')
        ds1_list.append(ds1)
    except Exception as e:
        pass
        
    try:
        ds1['v_wind_component'] = ds1['v']
        ds1 = ds1.drop_vars('v')
        ds1_list.append(ds1)
    except Exception as e:
        pass
    
    try:
        ds1['air_temperature'] = ds1['t']
        ds1 = ds1.drop_vars('t')
        ds1_list.append(ds1)
    except Exception as e:
        pass
    

    try:
        ds1['vertical_velocity'] = ds1['w']
        ds1 = ds1.drop_vars('w')
        ds1_list.append(ds1)
    except Exception as e:
        pass
    
    try:
        ds1 = _xr.concat(ds11_list, dim="time")
        ds1 = ds1.isel(time=0)
    except Exception as e:
        pass
        
    #################
    # Surface Level #
    #################
    
    ds2_list = []
    
    try:
        ds2['100m_u_wind_component'] = ds2['u100']
        ds2 = ds2.drop_vars('u100')
        ds2_list.append(ds2)
    except Exception as e:
        pass
    

    try:
        ds2['100m_v_wind_component'] = ds2['v100']
        ds2 = ds2.drop_vars('v100')
        ds2_list.append(ds2)
    except Exception as e:
        pass
    
    try:
        ds2 = _xr.concat(ds2_list, dim='time')
        ds2 = ds2.isel(time=0)
    except Exception as e:
        pass
    
    try:
        ds3['10m_u_wind_component'] = ds3['u10']
        ds3 = ds3.drop_vars('u10')
    except Exception as e:
        pass
    

    try:
        ds4['10m_v_wind_component'] = ds4['v10']
        ds4 = ds4.drop_vars('v10')
    except Exception as e:
        pass
        

    try:
        ds5['2m_temperature'] = ds5['t2m']
        ds5 = ds5.drop_vars('t2m')
    except Exception as e:
        pass
    

    try:
        ds6['2m_dew_point'] = ds6['d2m']
        ds6 = ds6.drop_vars('d2m')
    except Exception as e:
        pass
    
    
    ds7_list = []
    
    try:
        ds7['water_runoff'] = ds7['rowe']
        ds7 = ds7.drop_vars('rowe')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['surface_geopotential_height'] = ds7['z']
        ds7 = ds7.drop_vars('z')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['skin_temperature'] = ds7['skt']
        ds7 = ds7.drop_vars('skt')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['surface_pressure'] = ds7['sp']
        ds7 = ds7.drop_vars('sp')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['standard_deviation_of_sub_gridscale_orography'] = ds7['sdor']
        ds7 = ds7.drop_vars('sdor')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['slope_of_sub_gridscale_orography'] = ds7['slor']
        ds7 = ds7.drop_vars('slor')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['surface_shortwave_radiation_downward'] = ds7['ssrd']
        ds7 = ds7.drop_vars('ssrd')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['land_sea_mask'] = ds7['lsm']
        ds7 = ds7.drop_vars('lsm')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['surface_longwave_radiation_downward'] = ds7['strd']
        ds7 = ds7.drop_vars('strd')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['convective_precipitation'] = ds7['cp']
        ds7 = ds7.drop_vars('cp')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['snowfall_water_equivalent'] = ds7['sf']
        ds7 = ds7.drop_vars('sf')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    

    try:
        ds7['total_precipitation'] = ds7['tp']
        ds7 = ds7.drop_vars('tp')
        ds7_list.append(ds7)
    except Exception as e:
        pass
    
    try:
        ds7 = _xr.concat(ds7_list, dim="time")
        ds7 = ds7.isel(time=0)
    except Exception as e:
        pass
    

    try:
        ds8['low_cloud_cover'] = ds8['lcc']
        ds8 = ds8.drop_vars('lcc')
    except Exception as e:
        pass
    

    try:
        ds9['middle_cloud_cover'] = ds9['mcc']
        ds9 = ds9.drop_vars('mcc')
    except Exception as e:
        pass
    

    try:
        ds10['high_cloud_cover'] = ds10['hcc']
        ds10 = ds10.drop_vars('hcc')
        
    except Exception as e:
        pass
    
    ds11_list = []
    

    try:
        ds11['total_column_water'] = ds11['tcw']
        ds11 = ds11.drop_vars('tcw')
        ds11_list.append(ds11)
    except Exception as e:
        pass
    

    try:
        ds11['total_cloud_cover'] = ds11['tcc']
        ds11 = ds11.drop_vars('tcc')
        ds11_list.append(ds11)
    except Exception as e:
        pass
        
    try:
        ds11 = _xr.concat(ds11_list, dim="time")
        ds11 = ds11.isel(time=0)
    except Exception as e:
        pass
    

    try:
        ds12['mslp'] = ds12['msl']
        ds12 = ds12.drop_vars('msl')
    except Exception as e:
        pass
    
    
    _clear_idx_files_in_path(path)
    
    try:
    
        surface_ds_list = [ds0, ds1, ds2, ds3, ds4, ds5, ds6, ds7, ds8, ds9, ds10, ds11, ds12]
        
        surface_ds = []
        for d in surface_ds_list:
            if d is not None:
                try:
                    d = d.isel(time=0)
                except Exception as e:
                    pass
                surface_ds.append(d)
            else:
                pass
        
        ds = _xr.concat(surface_ds, 
                        dim='time', 
                        coords='minimal',
                        compat='override')
        
        try:
            ds = ds.drop_vars('sot')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('vsw')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('z')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('q')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('u')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('v')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('t')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('w')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('u100')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('v100')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('t2m')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('u10')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('v10')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('strd')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('d2m')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('rowe')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('z')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('skt')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sp')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sdor')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('slor')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('ssrd')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('lsm')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('strd')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('cp')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('sf')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('tp')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('lcc')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('mcc')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('hcc')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('tcw')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('tcc')
        except Exception as e:
            pass
        try:
            ds = ds.drop_vars('msl')
        except Exception as e:
            pass
        
        try:
            ds['2m_relative_humidity'] = _relative_humidity(ds['2m_temperature'],
                                                        ds['2m_dew_point'])
        except Exception as e:
            pass
        
        try:
            ds['2m_dew_point_depression'] = ds['2m_temperature'] - ds['2m_dew_point']
        except Exception as e:
            pass
        
        ds = ds.isel(time=0)
        
        try:
            ds = ds.transpose("number", "step", "latitude", "longitude")
        except Exception as e:
            pass
        
    except Exception as e:
        pass
        
    try:    
        ds = ds.sortby('step')
        return ds
    except Exception as e:
       _eccodes_error_message()
       _sys.exit(1)
    


def ecmwf_ifs_wave_post_processing(path,
                            western_bound, 
                            eastern_bound, 
                            northern_bound, 
                            southern_bound):
    
    """
    This function does the following:
    
    1) Subsets the ECMWF IFS Wave model data. 
    
    2) Post-processes the GRIB variable keys into Plain Language variable keys.
    
    Required Arguments:
    
    1) path (String) - The path to the folder containing the ECMWF IFS Wave files. 
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of ECMWF data.    
    
    Plain Language ECMWF IFS Wave Variable Keys 
    -------------------------------------------
    
    'mean_zero_crossing_wave_period'
    'significant_height_of_combined_waves_and_swell'
    'mean_wave_direction'
    'peak_wave_period'
    'mean_wave_period'

    """
    _clear_idx_files_in_path(path)
    
    files = _sorted_paths(path)
    
    try:
        ds = _xr.open_mfdataset(files, 
                            concat_dim='step', 
                            combine='nested', 
                            coords='minimal', 
                            engine='cfgrib', 
                            compat='override', 
                            decode_timedelta=False).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                        latitude=slice(northern_bound, southern_bound, 1))
    except Exception as e:
        pass
    
    try:
        ds['mean_zero_crossing_wave_period'] = ds['mp2']
        ds = ds.drop_vars('mp2')
    except Exception as e:
        pass
    
    try:
        ds['significant_height_of_combined_waves_and_swell'] = ds['swh']
        ds = ds.drop_vars('swh')
    except Exception as e:
        pass
    
    try:
        ds['mean_wave_direction'] = ds['mwd']
        ds = ds.drop_vars('mwd')
    except Exception as e:
        pass
    
    try:
        ds['peak_wave_period'] = ds['pp1d']
        ds = ds.drop_vars('pp1d')
    except Exception as e:
        pass
    
    try:
        ds['mean_wave_period'] = ds['mwp']
        ds = ds.drop_vars('mwp')
    except Exception as e:
        pass
    
    _clear_idx_files_in_path(path)
    
    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message()
        _sys.exit(1)
    return ds