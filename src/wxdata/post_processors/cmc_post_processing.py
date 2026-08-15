"""
This file hosts the function responsible for GDPS data post-processing. 

GRIB variable keys will be post-processed into Plain Language variable keys. 

(C) Eric J. Drewitz 2025-2026
"""
import xarray as _xr
import numpy as _np
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.warnings import eccodes_warning as _eccodes_warning
from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.utils.coords import(
    shift_longitude as _shift_longitude,
    convert_lon as _convert_lon
)

_eccodes_warning()
_sys.tracebacklimit = 0
_logging.disable()
   

def gdps_post_processing(path,
                         western_bound,
                         eastern_bound,
                         northern_bound,
                         southern_bound,
                         variable=None):
    
    """
    This function processes the model data from the GDPS by doing the following:
    
    1) Re-mapping the GRIB variable keys into a plain-language format.
    
    2) Trimming the data to fit the coordinates of your bounding box.
    
    3) Transform ds['longitude'] from a 0 to 360 coordinate system to -180 to 180 for the GDPS.
    
    Required Arguments:
    
    1) path (String) - The path to the directory holding the GRIB2 Data from CMC.
    
    2) western_bound (Float or Integer) - Default=-180. The western bound of the data needed. 

    3) eastern_bound (Float or Integer) - Default=180. The eastern bound of the data needed.

    4) northern_bound (Float or Integer) - Default=90. The northern bound of the data needed.

    5) southern_bound (Float or Integer) - Default=-90. The southern bound of the data needed.
    
    Optional Arguments:
    
    1) variable (String) - Default=None. For parameters that are unrecognized by eccodes, users can rename their
        parameter from 'unknown' to `variable`. 
        
    Returns
    -------    
    
    An xarray.array of the latest GDPS forecast data for a user-specified variable, level/layer and level_type.
    """


    western_bound, eastern_bound = _convert_lon(western_bound, 
                                                eastern_bound) 

    try:
        ds = _xr.open_mfdataset(f"{path}/*grib2",
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""}).sel(longitude=slice(western_bound, eastern_bound, 1), 
                                                                                                latitude=slice(southern_bound, northern_bound, 1))
        
        ds = _shift_longitude(ds)
    except Exception as e:
        pass
    
    
    try:
        ds['absolute_vorticity'] = ds['absv']
        ds = ds.drop_vars('absv')
    except Exception as e:
        pass
    
    try:
        ds['relative_vorticity'] = ds['vo']
        ds = ds.drop_vars('vo')
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    
    try:
        ds['albedo'] = ds['al']
        ds = ds.drop_vars('al')
    except Exception as e:
        pass
    
    try:
        ds['2m_temperature'] = ds['t2m']
        ds = ds.drop_vars('t2m')
    except Exception as e:
        pass
    
    try:
        if variable == 'cin':
            ds[variable] = _np.abs(ds['unknown'])
        else:
            if ' ' in variable:
                variable = variable.replace(' ', '_')
                ds[variable] = ds['unknown']
            else:
                ds[variable] = ds['unknown']
        ds = ds.drop_vars('unknown')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['tirf']
        ds = ds.drop_vars('tirf')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['iprate']
        ds = ds.drop_vars('iprate')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['fzrawe']
        ds = ds.drop_vars('fzrawe')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['tsnowp']
        ds = ds.drop_vars('tsnowp')
    except Exception as e:
        pass
    
    try:
        ds['cloud_water'] = ds['cwat']
        ds = ds.drop_vars('cwat')
    except Exception as e:
        pass
    
    try:
        ds['total_convective_precipitation'] = ds['acpcp']
        ds = ds.drop_vars('acpcp')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds['d2m']
        ds = ds.drop_vars('d2m')
    except Exception as e:
        pass
    
    try:
        ds['surface_downward_longwave_radiation_flux'] = ds['strd']
        ds = ds.drop_vars('strd')
    except Exception as e:
        pass
    
    try:
        ds['nominal_top_downward_shortwave_radiation_flux'] = ds['tisr']
        ds = ds.drop_vars('tisr')
    except Exception as e:
        pass
    
    try:
        ds['surface_downward_shortwave_radiation_flux'] = ds['ssrd']
        ds = ds.drop_vars('ssrd')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass
    
    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass
    
    try:
        ds['humidex'] = ds['hmdx']
        ds = ds.drop_vars('hmdx')
    except Exception as e:
        pass
    
    try:
        ds['k_index'] = ds['kx']
        ds = ds.drop_vars('kx')
    except Exception as e:
        pass
    
    try:
        ds['land_water_proportion'] = ds['lsm']
        ds = ds.drop_vars('lsm')
    except Exception as e:
        pass
    
    try:
        ds['latent_heat_net_flux'] = ds['slhtf']
        ds = ds.drop_vars('slhtf')
    except Exception as e:
        pass
    
    try:
        ds['lifted_index'] = ds['lftx4']
        ds = ds.drop_vars('lftx4')
    except Exception as e:
        pass
    
    try:
        ds['net_longwave_radiation_flux'] = ds['nlwrs']
        ds = ds.drop_vars('nlwrs')
    except Exception as e:
        pass
    
    try:
        ds['net_shortwave_radiation_flux'] = ds['nswrs']
        ds = ds.drop_vars('nswrs')
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds['o3']
        ds = ds.drop_vars('o3')
    except Exception as e:
        pass
    
    try:
        ds['boundary_layer_height'] = ds['blh']
        ds = ds.drop_vars('blh')
    except Exception as e:
        pass
    
    try:
        ds['precipitation_type'] = ds['ptype']
        ds = ds.drop_vars('ptype')
    except Exception as e:
        pass
    
    try:
        ds['mean_sea_level_pressure'] = ds['prmsl']
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass
    
    try:
        ds['air_pressure'] = ds['pres']
        ds = ds.drop_vars('pres')
    except Exception as e:
        pass
    
    try:
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass
    
    try:
        ds['radiative_temperature'] = ds['skt']
        ds = ds.drop_vars('skt')
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = ds['r2']
        ds = ds.drop_vars('r2')
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass
    
    try:
        ds['surface_runoff'] = ds['sro']
        ds = ds.drop_vars('sro')
    except Exception as e:
        pass
    
    try:
        ds['sea_ice_fraction'] = ds['siconc']
        ds = ds.drop_vars('siconc')
    except Exception as e:
        pass
    
    try:
        ds['sea_surface_temperature'] = ds['sst']
        ds = ds.drop_vars('sst')
    except Exception as e:
        pass
    
    try:
        ds['sensible_heat_net_flux'] = ds['ishf']
        ds = ds.drop_vars('ishf')
    except Exception as e:
        pass
    
    try:
        ds['snow_depth'] = ds['sde']
        ds = ds.drop_vars('sde')
    except Exception as e:
        pass
    
    try:
        ds['soil_temperature'] = ds['st']
        ds = ds.drop_vars('st')
    except Exception as e:
        pass
    
    try:
        ds['soil_volumetric_ice_content'] = ds['vsi']
        ds = ds.drop_vars('vsi')
    except Exception as e:
        pass
    
    try:
        ds['soil_volumetric_water_content'] = ds['vsw']
        ds = ds.drop_vars('vsw')
    except Exception as e:
        pass
    
    try:
        ds['2m_specific_humidity'] = ds['sh2']
        ds = ds.drop_vars('sh2')
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds['q']
        ds = ds.drop_vars('q')
    except Exception as e:
        pass
    
    try:
        ds['thickness'] = ds['thick']
        ds = ds.drop_vars('thick')
    except Exception as e:
        pass
    
    try:
        ds['total_totals_index'] = ds['totalx']
        ds = ds.drop_vars('totalx')
    except Exception as e:
        pass
    
    try:
        ds['uv_index_clear_sky'] = ds['uviucs']
        ds = ds.drop_vars('uviucs')
    except Exception as e:
        pass
    
    try:
        ds['uv_index'] = ds['uvi']
        ds = ds.drop_vars('uvi')
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds['w']
        ds = ds.drop_vars('w')
    except Exception as e:
        pass
    
    try:
        ds['wind_chill'] = ds['wcf']
        ds = ds.drop_vars('wcf')
    except Exception as e:
        pass
    
    try:
        ds['10m_wind_direction'] = ds['wdir10']
        ds = ds.drop_vars('wdir10')
    except Exception as e:
        pass
    
    try:
        ds['wind_direction'] = ds['wdir']
        ds = ds.drop_vars('wdir')
    except Exception as e:
        pass
    
    try:
        ds['10m_maximum_wind_gust'] = ds['fg10']
        ds = ds.drop_vars('fg10')
    except Exception as e:
        pass
    
    try:
        ds['10m_minimum_wind_gust'] = ds['min_i10fg']
        ds = ds.drop_vars('min_i10fg')
    except Exception as e:
        pass
    
    try:
        ds['10m_wind_gust'] = ds['i10fg']
        ds = ds.drop_vars('i10fg')
    except Exception as e:
        pass
    
    try:
        ds['10m_wind_speed'] = ds['si10']
        ds = ds.drop_vars('si10')
    except Exception as e:
        pass
    
    try:
        ds['wind_speed'] = ds['ws']
        ds = ds.drop_vars('ws')
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds['u10']
        ds = ds.drop_vars('u10')
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds['u']
        ds = ds.drop_vars('u')
    except Exception as e:
        pass
    
    try:
        ds['10m_v_wind_component'] = ds['v10']
        ds = ds.drop_vars('v10')
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component'] = ds['v']
        ds = ds.drop_vars('v')
    except Exception as e:
        pass    
    
    try:
        ds['precipitation_rate'] = ds['prate']
        ds = ds.drop_vars('prate')
    except Exception as e:
        pass

    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message() 

    try:
        ds = ds.drop_duplicates(dim='step', keep='first')
    except Exception as e:
        pass

    
    return ds


def rdps_post_processing(path,
                         variable=None):
    
    """
    This function processes the model data from the RDPS by doing the following:
    
    1) Re-mapping the GRIB variable keys into a plain-language format.
    
    2) Trimming the data to fit the coordinates of your bounding box.
    
    3) Transform ds['longitude'] from a 0 to 360 coordinate system to -180 to 180 for the GDPS.
    
    Required Arguments:
    
    1) path (String) - The path to the directory holding the GRIB2 Data from CMC.
    
    Optional Arguments:
    
    1) variable (String) - Default=None. For parameters that are unrecognized by eccodes, users can rename their
        parameter from 'unknown' to `variable`. 
        
    Returns
    -------    
    
    An xarray.array of the latest GDPS forecast data for a user-specified variable, level/layer and level_type.
    """

    try:
        ds = _xr.open_mfdataset(f"{path}/*grib2",
                                concat_dim='step', 
                                combine='nested', 
                                coords='minimal', 
                                engine='cfgrib', 
                                compat='override', 
                                decode_timedelta=False,
                                backend_kwargs={"indexpath": ""}).sel(x=slice(180, 900, 1), 
                                                                      y=slice(0, 800, 1))
    except Exception as e:
        pass
    
    try:
        ds['absolute_vorticity'] = ds['absv']
        ds = ds.drop_vars('absv')
    except Exception as e:
        pass
    
    try:
        ds['relative_vorticity'] = ds['vo']
        ds = ds.drop_vars('vo')
    except Exception as e:
        pass
    
    try:
        ds['air_temperature'] = ds['t']
        ds = ds.drop_vars('t')
    except Exception as e:
        pass
    
    try:
        ds['albedo'] = ds['al']
        ds = ds.drop_vars('al')
    except Exception as e:
        pass
    
    try:
        ds['2m_temperature'] = ds['t2m']
        ds = ds.drop_vars('t2m')
    except Exception as e:
        pass
    
    try:
        if variable == 'cin':
            ds[variable] = _np.abs(ds['unknown'])
        else:
            if ' ' in variable:
                variable = variable.replace(' ', '_')
                ds[variable] = ds['unknown']
            else:
                ds[variable] = ds['unknown']
        ds = ds.drop_vars('unknown')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['tirf']
        ds = ds.drop_vars('tirf')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['iprate']
        ds = ds.drop_vars('iprate')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['fzrawe']
        ds = ds.drop_vars('fzrawe')
    except Exception as e:
        pass
    
    try:
        variable = variable.replace(' ', '_')
        ds[variable] = ds['tsnowp']
        ds = ds.drop_vars('tsnowp')
    except Exception as e:
        pass
    
    try:
        ds['cloud_water'] = ds['cwat']
        ds = ds.drop_vars('cwat')
    except Exception as e:
        pass
    
    try:
        ds['total_convective_precipitation'] = ds['acpcp']
        ds = ds.drop_vars('acpcp')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds['d2m']
        ds = ds.drop_vars('d2m')
    except Exception as e:
        pass
    
    try:
        ds['surface_downward_longwave_radiation_flux'] = ds['strd']
        ds = ds.drop_vars('strd')
    except Exception as e:
        pass
    
    try:
        ds['nominal_top_downward_shortwave_radiation_flux'] = ds['tisr']
        ds = ds.drop_vars('tisr')
    except Exception as e:
        pass
    
    try:
        ds['surface_downward_shortwave_radiation_flux'] = ds['ssrd']
        ds = ds.drop_vars('ssrd')
    except Exception as e:
        pass
    
    try:
        ds['geopotential_height'] = ds['gh']
        ds = ds.drop_vars('gh')
    except Exception as e:
        pass
    
    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass
    
    try:
        ds['humidex'] = ds['hmdx']
        ds = ds.drop_vars('hmdx')
    except Exception as e:
        pass
    
    try:
        ds['k_index'] = ds['kx']
        ds = ds.drop_vars('kx')
    except Exception as e:
        pass
    
    try:
        ds['land_water_proportion'] = ds['lsm']
        ds = ds.drop_vars('lsm')
    except Exception as e:
        pass
    
    try:
        ds['latent_heat_net_flux'] = ds['slhtf']
        ds = ds.drop_vars('slhtf')
    except Exception as e:
        pass
    
    try:
        ds['lifted_index'] = ds['lftx4']
        ds = ds.drop_vars('lftx4')
    except Exception as e:
        pass
    
    try:
        ds['net_longwave_radiation_flux'] = ds['nlwrs']
        ds = ds.drop_vars('nlwrs')
    except Exception as e:
        pass
    
    try:
        ds['net_shortwave_radiation_flux'] = ds['nswrs']
        ds = ds.drop_vars('nswrs')
    except Exception as e:
        pass
    
    try:
        ds['ozone_mixing_ratio'] = ds['o3']
        ds = ds.drop_vars('o3')
    except Exception as e:
        pass
    
    try:
        ds['boundary_layer_height'] = ds['blh']
        ds = ds.drop_vars('blh')
    except Exception as e:
        pass
    
    try:
        ds['precipitation_type'] = ds['ptype']
        ds = ds.drop_vars('ptype')
    except Exception as e:
        pass
    
    try:
        ds['mean_sea_level_pressure'] = ds['prmsl']
        ds = ds.drop_vars('prmsl')
    except Exception as e:
        pass
    
    try:
        ds['air_pressure'] = ds['pres']
        ds = ds.drop_vars('pres')
    except Exception as e:
        pass
    
    try:
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass
    
    try:
        ds['radiative_temperature'] = ds['skt']
        ds = ds.drop_vars('skt')
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = ds['r2']
        ds = ds.drop_vars('r2')
    except Exception as e:
        pass
    
    try:
        ds['relative_humidity'] = ds['r']
        ds = ds.drop_vars('r')
    except Exception as e:
        pass
    
    try:
        ds['surface_runoff'] = ds['sro']
        ds = ds.drop_vars('sro')
    except Exception as e:
        pass
    
    try:
        ds['sea_ice_fraction'] = ds['siconc']
        ds = ds.drop_vars('siconc')
    except Exception as e:
        pass
    
    try:
        ds['sea_surface_temperature'] = ds['sst']
        ds = ds.drop_vars('sst')
    except Exception as e:
        pass
    
    try:
        ds['sensible_heat_net_flux'] = ds['ishf']
        ds = ds.drop_vars('ishf')
    except Exception as e:
        pass
    
    try:
        ds['snow_depth'] = ds['sde']
        ds = ds.drop_vars('sde')
    except Exception as e:
        pass
    
    try:
        ds['soil_temperature'] = ds['st']
        ds = ds.drop_vars('st')
    except Exception as e:
        pass
    
    try:
        ds['soil_volumetric_ice_content'] = ds['vsi']
        ds = ds.drop_vars('vsi')
    except Exception as e:
        pass
    
    try:
        ds['soil_volumetric_water_content'] = ds['vsw']
        ds = ds.drop_vars('vsw')
    except Exception as e:
        pass
    
    try:
        ds['2m_specific_humidity'] = ds['sh2']
        ds = ds.drop_vars('sh2')
    except Exception as e:
        pass
    
    try:
        ds['specific_humidity'] = ds['q']
        ds = ds.drop_vars('q')
    except Exception as e:
        pass
    
    try:
        ds['thickness'] = ds['thick']
        ds = ds.drop_vars('thick')
    except Exception as e:
        pass
    
    try:
        ds['total_totals_index'] = ds['totalx']
        ds = ds.drop_vars('totalx')
    except Exception as e:
        pass
    
    try:
        ds['uv_index_clear_sky'] = ds['uviucs']
        ds = ds.drop_vars('uviucs')
    except Exception as e:
        pass
    
    try:
        ds['uv_index'] = ds['uvi']
        ds = ds.drop_vars('uvi')
    except Exception as e:
        pass
    
    try:
        ds['vertical_velocity'] = ds['w']
        ds = ds.drop_vars('w')
    except Exception as e:
        pass
    
    try:
        ds['wind_chill'] = ds['wcf']
        ds = ds.drop_vars('wcf')
    except Exception as e:
        pass
    
    try:
        ds['10m_wind_direction'] = ds['wdir10']
        ds = ds.drop_vars('wdir10')
    except Exception as e:
        pass
    
    try:
        ds['wind_direction'] = ds['wdir']
        ds = ds.drop_vars('wdir')
    except Exception as e:
        pass
    
    try:
        ds['10m_maximum_wind_gust'] = ds['fg10']
        ds = ds.drop_vars('fg10')
    except Exception as e:
        pass
    
    try:
        ds['10m_minimum_wind_gust'] = ds['min_i10fg']
        ds = ds.drop_vars('min_i10fg')
    except Exception as e:
        pass
    
    try:
        ds['10m_wind_gust'] = ds['i10fg']
        ds = ds.drop_vars('i10fg')
    except Exception as e:
        pass
    
    try:
        ds['10m_wind_speed'] = ds['si10']
        ds = ds.drop_vars('si10')
    except Exception as e:
        pass
    
    try:
        ds['wind_speed'] = ds['ws']
        ds = ds.drop_vars('ws')
    except Exception as e:
        pass
    
    try:
        ds['10m_u_wind_component'] = ds['u10']
        ds = ds.drop_vars('u10')
    except Exception as e:
        pass
    
    try:
        ds['u_wind_component'] = ds['u']
        ds = ds.drop_vars('u')
    except Exception as e:
        pass
    
    try:
        ds['10m_v_wind_component'] = ds['v10']
        ds = ds.drop_vars('v10')
    except Exception as e:
        pass
    
    try:
        ds['v_wind_component'] = ds['v']
        ds = ds.drop_vars('v')
    except Exception as e:
        pass    
    
    try:
        ds['precipitation_rate'] = ds['prate']
        ds = ds.drop_vars('prate')
    except Exception as e:
        pass
    
    try:
        ds['sweat_index'] = ds['sx']
        ds = ds.drop_vars('sx')
    except Exception as e:
        pass
    
    try:
        ds['storm_relative_helicity'] = ds['hlcy']
        ds = ds.drop_vars('hlcy')
    except Exception as e:
        pass
    
    try:
        ds['vertical_wind_shear'] = ds['vwsh']
        ds = ds.drop_vars('vwsh')
    except Exception as e:
        pass

    try:    
        ds = ds.sortby('step')
    except Exception as e:
        _eccodes_error_message() 

    try:
        ds = ds.drop_duplicates(dim='step', keep='first')
    except Exception as e:
        pass

    
    return ds


