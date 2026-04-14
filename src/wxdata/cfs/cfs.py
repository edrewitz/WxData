"""
This file hosts the CFS data clients that directly interact with the user.

1) cfs_flux()
2) cfs_pressure()

(C) Eric J. Drewitz 2025-2026
"""

import wxdata.client.client as _client
import wxdata.post_processors.cfs_post_processing as _cfs_post_processing
import os as _os 
import warnings as _warnings
_warnings.filterwarnings('ignore')

from wxdata.cfs.url_scanners import(
    cfs_flux_url_scanner as _cfs_flux_url_scanner,
    cfs_pressure_url_scanner as _cfs_pressure_url_scanner
)
from wxdata.cfs.file_scanner import cfs_file_scanner as _cfs_file_scanner
from wxdata.calc.unit_conversion import convert_temperature_units as _convert_temperature_units
from wxdata.utils.recycle_bin import(
    clear_recycle_bin_windows as _clear_recycle_bin_windows,
    clear_trash_bin_mac as _clear_trash_bin_mac,
    clear_trash_bin_linux as _clear_trash_bin_linux
)

def cfs_flux(western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            proxies=None, 
            clear_recycle_bin=False,
            clear_data=False,
            chunk_size=8192,
            notifications='off',
            path=f"CFS/FLUX",
            variables=['aerodynamic conductance',
                        'albedo',
                        'clear sky uv-b downward solar flux',
                        'plant canopy surface water',
                        'convective precipitation rate',
                        'categorical rain',
                        'clear sky downward longwave flux',
                        'clear sky downward solar flux (surface)',
                        'clear sky downward solar flux (top of the atmosphere)',
                        'clear sky upward solar flux',
                        'cloud work function',
                        'downward longwave radiation flux',
                        'downward shortwave radiation flux',
                        'clear sky uv-b downward solar flux',
                        'direct evaporation from bare soil',
                        'canopy water evaporation',
                        'surface friction velocity',
                        'ground heat flux',
                        'geopotential height',
                        'planetary boundary layer height',
                        'ice cover',
                        'ice thickness',
                        'land cover',
                        'latent heat net flux',
                        'near ir beam downward solar flux',
                        'near ir diffuse downward solar flux',
                        'potential evaporation rate',
                        'precipitation rate',
                        'pressure',
                        'precipitable water',
                        '2-meter maximum specific humidity',
                        '2-meter minimum specific humidity',
                        'sublimation (evaporation from snow)',
                        'surface roughness',
                        'sedimentation mass flux',
                        'sensible heat net flux',
                        'surface slope type',
                        'snow depth',
                        'snow phase-change heat flux',
                        'snow cover',
                        'liquid volumetric soil moisture (non-frozen)',
                        'soil moisture content',
                        'volumetric soil moisture content',
                        'soil type',
                        'specific humidity',
                        'snowfall rate water equivalent',
                        'storm surface runoff (non-infiltrating)',
                        'total cloud cover',
                        'maximum temperature',
                        'minimum temperature',
                        'temperature',
                        'transpiration',
                        'momentum flux (u-component)',
                        'u-component of wind',
                        'zonal flux of gravity wave stress',
                        'upward longwave radiation flux',
                        'upward shortwave radiation flux',
                        'visible beam downward solar flux',
                        'vegetation',
                        'momentum flux (v-component)',
                        'v-component of wind',
                        'vegetation type',
                        'meridional flux of gravity wave stress',
                        'water runoff',
                        'water equivalent of accumulated snow depth']):
    
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass  
    
    try:
        _os.makedirs(f"{path}")
    except Exception as e:
        pass
    
    
    urls, files = _cfs_flux_url_scanner(western_bound, 
                                        eastern_bound, 
                                        northern_bound, 
                                        southern_bound, 
                                        proxies, 
                                        variables)
    
    download = _cfs_file_scanner(path,
                                 files)
    
    if clear_data == True:
        download = True
    else:
        pass
    
    if download == True:
        try:
            for file in _os.listdir(f"{path}"):
                _os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        print(f"Downloading Latest CFS Data")
        
        for url, filename in zip(urls, files):    
        
            _client.get_gridded_data(url,
                                     path,
                                     filename,
                                     proxies=proxies,
                                     chunk_size=chunk_size,
                                     notifications=notifications)
    else:
        print(f"Data in local directory is current. Skipping Download")
        
        
def cfs_pressure(western_bound=-180, 
            eastern_bound=180, 
            northern_bound=90, 
            southern_bound=-90, 
            final_forecast_hour=384,
            proxies=None, 
            clear_recycle_bin=False,
            clear_data=False,
            chunk_size=8192,
            notifications='off',
            path=f"CFS/PRESSURE",
            process_data=True,
            convert_temperature=True,
            convert_to='celsius',
            variables=['best lifted index',
                        '5 wave geopotential height anomaly',
                        '5 wave geopotential height',
                        'absolute vorticity',
                        'convective precipitation',
                        'total precipitation',
                        'convective available potential energy',
                        'categorical freezing rain',
                        'categorical ice pellets',
                        'convective inhibition',
                        'cloud mixing ratio',
                        'categorical rain',
                        'categorical snow',
                        'cloud water',
                        'dew point',
                        'geopotential height anomaly',
                        'geopotential height',
                        'storm relative helicity',
                        'surface lifted index',
                        'large scale non-convective precipitation',
                        'ozone mixing ratio',
                        'parcel lifted index (to 500mb)',
                        'potential temperature',
                        'pressure',
                        'mean sea level pressure',
                        'precipitable water',
                        'relative humidity',
                        'specific humidity',
                        'stream function',
                        'temperature',
                        'total ozone',
                        'u-component of wind',
                        'u-component of storm motion',
                        'v-component of wind',
                        'velocity potential',
                        'v-component of storm motion',
                        'vertical velocity (pressure)',
                        'vertical speed shear']):
    
    
    if clear_recycle_bin == True:
        _clear_recycle_bin_windows()
        _clear_trash_bin_mac()
        _clear_trash_bin_linux()
    else:
        pass  
    
    try:
        _os.makedirs(f"{path}")
    except Exception as e:
        pass
    
    
    urls, files = _cfs_pressure_url_scanner(western_bound, 
                                        eastern_bound, 
                                        northern_bound, 
                                        southern_bound, 
                                        proxies, 
                                        variables,
                                        final_forecast_hour)
    
    download = _cfs_file_scanner(path,
                                 files)
    
    if clear_data == True:
        download = True
    else:
        pass
    
    if download == True:
        try:
            for file in _os.listdir(f"{path}"):
                _os.remove(f"{path}/{file}")
        except Exception as e:
            pass
        
        print(f"Downloading Latest CFS Pressure Data")
        
        for url, filename in zip(urls, files):    
        
            _client.get_gridded_data(url,
                                     path,
                                     filename,
                                     proxies=proxies,
                                     chunk_size=chunk_size,
                                     notifications=notifications)
    else:
        print(f"Data in local directory is current. Skipping Download")
        
    if process_data == True:
        print(f"CFS Pressure Data Processing...")
        
        ds = _cfs_post_processing.cfs_pressure_post_processing(path)
        
        if convert_temperature == True:
                ds = _convert_temperature_units(ds, 
                                            convert_to)
                
        else:
            pass
        
        print(f"CFS Pressure Data Processing Complete.")
        return ds
    
    else:
        pass 
    
    