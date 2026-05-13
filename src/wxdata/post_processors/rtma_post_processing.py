"""
This file hosts the function that preprocesses RTMA Data. 

(C) Eric J. Drewitz 2025-2026
"""
    
import xarray as _xr
import numpy as _np
import metpy.calc as _mpcalc
import sys as _sys
import logging as _logging
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.utils.exceptions import eccodes_error_message as _eccodes_error_message
from wxdata.calc.thermodynamics import relative_humidity as _relative_humidity
from wxdata.utils.file_funcs import clear_idx_files_in_path as _clear_idx_files_in_path
from wxdata.utils.coords import shift_longitude as _shift_longitude_regrid

_sys.tracebacklimit = 0
_logging.disable()

def _shift_longitude(ds):
    
    """
    This function shifts the longitude of dimension (x,y) from 0 to 360 to -180 to 180
    
    Required Arguments:
    
    1) ds (xarray.array) - The xarray data array of RTMA Data
    
    Optional Arguments: None
    
    Returns
    -------
    
    A RTMA dataset with longitude from -180 to 180    
    """
    
    lon = ((ds['longitude'].values + 180.0) % 360.0) - 180.0
    
    ds = ds.assign(
    longitude=(("y", "x"), lon)
    )
    
    return ds

def _rows_and_cols(model):
    
    """
    This function returns the number of rows and columns for the low-latitude island RTMA datasets.
    
    This is needed to resolve the "1-D Data Problem" in these datasets. 
    
    Required Arguments: 
    
    1) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    Optional Arguments: None
    
    Returns
    -------
    
    The number of rows and columns for post-processing the 1-D RTMA Datasets    
    """
    model = model.upper()
    
    dims = {
        
        'HI RTMA':[225, 321],
        'PR RTMA':[176, 251],
        'GU RTMA':[193, 193]
    }
    
    return dims[model][0], dims[model][1]

def process_rtma_data(
                     path,
                     filename, 
                     model,
                     ):
    
    """
    This function post-processes RTMA Data and returns an xarray data array of the data.
    
    This post-processing will convert all variable names into a plain language format. 
    
    
    Required Arguments: 
    
    1) path (String) - The path to the file that has the RTMA Data. 
    
    2) model (String) - Default='rtma'. The RTMA model being used:
    
    RTMA Models
    -----------
    
    CONUS = 'rtma'
    Alaska = 'ak rtma'
    Hawaii = 'hi rtma'
    Puerto Rico = 'pr rtma'
    Guam = 'gu rtma'
    
    3) directory (String) - The directory path where the RTMA files are saved to. 
    
    Optional Arguments: None
    
    Returns
    -------
    
    An xarray data array of the RTMA Dataset with variable keys converted from the GRIB format to a Plain Language format. 
    
    Variable Keys
    -------------
    
    'orography'
    'surface_pressure'
    '2m_temperature'
    '2m_dew_point'
    '2m_relative_humidity'
    '2m_specific_humidity'
    'surface_visibility'
    'cloud_ceiling_height'
    'total_cloud_cover'
    '10m_u_wind_component'
    '10m_v_wind_component'
    '10m_wind_direction'
    '10m_wind_speed'
    '10m_wind_gust'
        
    """
    model = model.upper()
    
    _clear_idx_files_in_path(path)

    try:
        ds = _xr.open_dataset(f"{path}/{filename}", engine='cfgrib',
                              backend_kwargs={"indexpath": ""})
    except Exception as e:
        _eccodes_error_message()
        _sys.exit(1)
    
    try:
        ds['orography'] = ds['orog']
        ds = ds.drop_vars('orog')
    except Exception as e:
        pass
    
    try:
        ds['surface_pressure'] = ds['sp']
        ds = ds.drop_vars('sp')
    except Exception as e:
        pass
    
    try:
        ds['2m_temperature'] = ds['t2m']
        ds = ds.drop_vars('t2m')
    except Exception as e:
        pass
    
    try:
        ds['2m_dew_point'] = ds['d2m']
        ds = ds.drop_vars('d2m')
    except Exception as e:
        pass
    
    try:
        ds['2m_relative_humidity'] = _relative_humidity(ds['2m_temperature'], ds['2m_dew_point'])
    except Exception as e:
        pass
    
    try:
        ds['2m_specific_humidity'] = ds['sh2']
        ds = ds.drop_vars('sh2')
    except Exception as e:
        pass
    try:
        ds['surface_visibility'] = ds['vis']
        ds = ds.drop_vars('vis')
    except Exception as e:
        pass
    
    try:
        ds['cloud_ceiling_height'] = ds['ceil']
        ds = ds.drop_vars('ceil')
    except Exception as e:
        pass
    
    try:
        ds['total_cloud_cover'] = ds['tcc']
        ds = ds.drop_vars('tcc')
    except Exception as e:
        pass
    
    try:
        ds1 = _xr.open_dataset(f"{path}/{filename}", 
                            engine='cfgrib', 
                            decode_timedelta=False, 
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10u'},
                            backend_kwargs={"indexpath": ""})
        ds['10m_u_wind_component'] = ds1['u10']
    except Exception as e:
        pass
    
    try:
        ds2 = _xr.open_dataset(f"{path}/{filename}", 
                            engine='cfgrib', 
                            decode_timedelta=False, 
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10v'},
                            backend_kwargs={"indexpath": ""})
        ds['10m_v_wind_component'] = ds2['v10']   
    except Exception as e:
        pass 
    
    try:
        ds3 = _xr.open_dataset(f"{path}/{filename}", 
                            engine='cfgrib', 
                            decode_timedelta=False, 
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10wdir'},
                            backend_kwargs={"indexpath": ""})
        ds['10m_wind_direction'] = ds3['wdir10']
    except Exception as e:
        pass
    
    try:
        ds4 = _xr.open_dataset(f"{path}/{filename}", 
                            engine='cfgrib', 
                            decode_timedelta=False, 
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'10si'},
                            backend_kwargs={"indexpath": ""})
        ds['10m_wind_speed'] = ds4['si10']
    except Exception as e:
        pass
    
    try:
        ds5 = _xr.open_dataset(f"{path}/{filename}",
                            engine='cfgrib',
                            decode_timedelta=False, 
                            filter_by_keys={'typeOfLevel': 'heightAboveGround','shortName':'i10fg'},
                            backend_kwargs={"indexpath": ""})
        ds['10m_wind_gust'] = ds5['i10fg']
    except Exception as e:
        pass
    
    if model == 'HI RTMA' or model == 'GU RTMA' or model == 'PR RTMA':
        
        nrows, ncols = _rows_and_cols(model)
        
        try:
            orog = ds['orography'].values
        except Exception as e:
            pass
        try:
            pressure = ds['surface_pressure'].values
        except Exception as e:
            pass           
        try:    
            temp = ds['2m_temperature'].values
        except Exception as e:
            pass        
        try:
            dwpt = ds['2m_dew_point'].values
        except Exception as e:
            pass        
        try:
            rh = ds['2m_relative_humidity'].values
        except Exception as e:
            pass        
        try:
            sh = ds['2m_specific_humidity'].values
        except Exception as e:
            pass        
        try:
            vis = ds['surface_visibility'].values
        except Exception as e:
            pass        
        try:
            ceil = ds['cloud_ceiling_height'].values
        except Exception as e:
            pass        
        try:
            tcc = ds['total_cloud_cover'].values
        except Exception as e:
            pass        
        try:
            u = ds['10m_u_wind_component'].values
        except Exception as e:
            pass        
        try:
            v = ds['10m_v_wind_component'].values
        except Exception as e:
            pass        
        try:
            wdir = ds['10m_wind_direction'].values
        except Exception as e:
            pass        
        try:
            ws = ds['10m_wind_speed'].values
        except Exception as e:
            pass        
        try:
            wgust = ds['10m_wind_gust'].values
        except Exception as e:
            pass        
        try:
            lat = ds['latitude'].values
        except Exception as e:
            pass        
        try:
            lon = ds['longitude'].values
        except Exception as e:
            pass        
        try:
            time = ds['time'].values
        except Exception as e:
            pass            
            
        try:
            orog_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            pressure_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            temp_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            dwpt_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            rh_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            sh_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            vis_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            ceil_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            tcc_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            u_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            v_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            wdir_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            ws_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            wgust_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            lat_2d = _np.empty([nrows,ncols])
        except Exception as e:
            pass        
        try:
            lon_2d = _np.empty([nrows,ncols])    
        except Exception as e:
            pass        
        
        
        for i in range(0,nrows):
            start = i*ncols
            end = start+ncols

            try:
                orog_2d[i,:] = orog[start:end]
            except Exception as e:
                pass            
            try:
                pressure_2d[i,:] = pressure[start:end]
            except Exception as e:
                pass              
            try:
                temp_2d[i,:] = temp[start:end]
            except Exception as e:
                pass              
            try:
                dwpt_2d[i,:] = dwpt[start:end]
            except Exception as e:
                pass              
            try:
                rh_2d[i,:] = rh[start:end]
            except Exception as e:
                pass              
            try:
                sh_2d[i,:] = sh[start:end]
            except Exception as e:
                pass              
            try:
                vis_2d[i,:] = vis[start:end]
            except Exception as e:
                pass              
            try:
                ceil_2d[i,:] = ceil[start:end]
            except Exception as e:
                pass              
            try:
                tcc_2d[i,:] = tcc[start:end]
            except Exception as e:
                pass              
            try:
                u_2d[i,:] = u[start:end]
            except Exception as e:
                pass              
            try:
                v_2d[i,:] = v[start:end]
            except Exception as e:
                pass              
            try:
                wdir_2d[i,:] = wdir[start:end]
            except Exception as e:
                pass              
            try:
                ws_2d[i,:] = ws[start:end]
            except Exception as e:
                pass              
            try:
                wgust_2d[i,:] = wgust[start:end]
            except Exception as e:
                pass  
            try:
                lat_2d[i,:] = lat[start:end]
            except Exception as e:
                pass              
            try:
                lon_2d[i,:] = lon[start:end]
            except Exception as e:
                pass  

        try:
            lon1d = lon_2d[0,:]
        except Exception as e:
            pass          
        try:
            lat1d = lat_2d[:,0]  
        except Exception as e:
            pass        
        dims = ("latitude", "longitude")
        coords = {
            "time":time,
            "latitude": lat1d,  
            "longitude": lon1d,  
        }
        try:
            ds1 = _xr.DataArray(orog_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds2 = _xr.DataArray(pressure_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds3 = _xr.DataArray(temp_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds4 = _xr.DataArray(dwpt_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds5 = _xr.DataArray(rh_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds6 = _xr.DataArray(sh_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds7 = _xr.DataArray(vis_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds8 = _xr.DataArray(ceil_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds9 = _xr.DataArray(tcc_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds10 = _xr.DataArray(u_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds11 = _xr.DataArray(v_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds12 = _xr.DataArray(wdir_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds13 = _xr.DataArray(ws_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
        try:    
            ds14 = _xr.DataArray(wgust_2d, 
                                coords=coords, 
                                dims=dims)
        except Exception as e:
            pass            
            
        try:    
            ds1['orography'] = ds1
        except Exception as e:
            pass            
        try:    
            ds1['surface_pressure'] = ds2
        except Exception as e:
            pass            
        try:    
            ds1['2m_temperature'] = ds3
        except Exception as e:
            pass            
        try:    
            ds1['2m_dew_point'] = ds4
        except Exception as e:
            pass            
        try:    
            ds1['2m_relative_humidity'] = ds5
        except Exception as e:
            pass            
        try:    
            ds1['2m_specific_humidity'] = ds6
        except Exception as e:
            pass            
        try:    
            ds1['surface_visibility'] = ds7
        except Exception as e:
            pass            
        try:    
            ds1['cloud_ceiling_height'] = ds8
        except Exception as e:
            pass            
        try:    
            ds1['total_cloud_cover'] = ds9
        except Exception as e:
            pass            
        try:    
            ds1['10m_u_wind_component'] = ds10
        except Exception as e:
            pass            
        try:    
            ds1['10m_v_wind_component'] = ds11
        except Exception as e:
            pass            
        try:    
            ds1['10m_wind_direction'] = ds12
        except Exception as e:
            pass            
        try:    
            ds1['10m_wind_speed'] = ds13
        except Exception as e:
            pass            
        try:    
            ds1['10m_wind_gust'] = ds14
        except Exception as e:
            pass            
            
        try:    
            ds1['surface_pressure'] = _mpcalc.smooth_gaussian(ds1['surface_pressure'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['2m_temperature'] = _mpcalc.smooth_gaussian(ds1['2m_temperature'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['2m_dew_point'] = _mpcalc.smooth_gaussian(ds1['2m_dew_point'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['2m_relative_humidity'] = _mpcalc.smooth_gaussian(ds1['2m_relative_humidity'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['2m_specific_humidity'] = _mpcalc.smooth_gaussian(ds1['2m_specific_humidity'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['surface_visibility'] = _mpcalc.smooth_gaussian(ds1['surface_visibility'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['cloud_ceiling_height'] = _mpcalc.smooth_gaussian(ds1['cloud_ceiling_height'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['total_cloud_cover'] = _mpcalc.smooth_gaussian(ds1['total_cloud_cover'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['10m_u_wind_component'] = _mpcalc.smooth_gaussian(ds1['10m_u_wind_component'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['10m_v_wind_component'] = _mpcalc.smooth_gaussian(ds1['10m_v_wind_component'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['10m_wind_direction'] = _mpcalc.smooth_gaussian(ds1['10m_wind_direction'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['10m_wind_speed'] = _mpcalc.smooth_gaussian(ds1['10m_wind_speed'], n=8)
        except Exception as e:
            pass            
        try:    
            ds1['10m_wind_gust'] = _mpcalc.smooth_gaussian(ds1['10m_wind_gust'], n=8)
        except Exception as e:
            pass        
        
                
        ds1 = _shift_longitude_regrid(ds1)
        
        return ds1
        
    else:
        
        ds = _shift_longitude(ds)
            
        return ds