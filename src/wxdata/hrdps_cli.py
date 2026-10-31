"""
This file hosts the WxData Command Line Interface for retrieving Canadian High Resolution Deterministic Prediction System (HRDPS) Data.

Command Line Use: `wxdata-hrdps **args`

(C) Eric J. Drewitz 2025-2026
"""
import click as _click
import sys as _sys
import platform as _platform
current_os = _platform.system()

from wxdata.model_data.cmc.hrdps.hrdps import hrdps as _fetch_hrdps

def _command_error_message(model):
    
    """Error Message For Invalid Commands"""
    
    print(f"\n\nInvalid Command Error: User Entered An Invalid Command.")
    print(f"Model: {model.upper()}")
    print(f"Please visit: https://edrewitz.github.io/WxData/HRDPS%20CLI for full detailed documentation.")

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
def hrdps_data():
    """HRDPS command line utilities."""
    pass

# ---------------------------------------------------------------------
# HRDPS Commands
# ---------------------------------------------------------------------
@hrdps_data.group(name='fetch')
def fetch_hrdps_data():
    
    r"""
    
    Canadian High Resolution Deterministic Prediction System (HRDPS) Command Line Interface
    
    ***Valid Commands***
    
    -f = Final Forecast Hour. Default=48.
    
    -cr = Clear Recycle Bin (Default=False).
    
    For users who want to ensure old files are completely deleted when automating data retrieval set -cr True.
    Setting -cr True clears your recycle bin with each run of the script. 
    This ensures if any old files are moved to the recycle bin are deleted if they are not already.
    
    -cd = Clear Data (Default=False).
    
    When set to False the scanner safeguard that prevents repetative downloads is enabled.
    Set -cd False to disable this safety feature.
    
    WARNING: When this feature is disabled and the user submits too many requests in a short period of time the user risks
    being rate-limited by the data server. If the user gets rate-limited, the user should wait approximately 5-10 minutes and
    retry downloading the data.  
    
    -cdir = Custom Directory (Default=None).
    
    If the user wishes to build their own directory to hold the data files set -cd directory_branch_path.

    -ct = Convert Temperature (Default=True).
    
    When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit.
    
    -tu = Temperature Units (Default=Celsius).
    
    When -ct True this is where you declare the units for temperature to be converted to. 
    
    -v = Variable. Variable to pass into the function. 
        
        Default='geopotential_height'
        
        ***Variables & Proper level_type & level***
    
        Any area where valid_levels = None -> Users do not need to edit the optional argument `level`
        
        'air density':
            valid level type(s) = 'height above ground', 'surface'.
            valid levels:
                level_type='height above ground' (m): 40, 80, 120 
                
                level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
        
        
        'absolute vorticity':
            valid level type(s): 'pressure'
            valid levels: 
                level_type='pressure' (hPa): 1000, 850, 700, 500, 250
        
        
        'albedo':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'blowing snow':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'boundary layer height':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'cape':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'character of precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'cloud water':
            valid level type(s): 'entire atmosphere'
            valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level)  
        
        
        'conditional freezing precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'conditional amount of liquid precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'conditional amount of solid ice pellets':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'conditional amount of solid snow':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'conditional precipitation rate':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'convective precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'dew point depression':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 2, 40, 80, 120
        
        
        'dew point':
            valid level type(s) = 'height above ground', 'surface'.
            valid levels:                      
                level_type='height above ground' (m): 2, 40, 80, 120
                
                level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
        
        
        'dominant precipitation type':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'downward longwave radiation flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'downward shortwave radiation flux':
            valid level type(s): 'surface', 'nominal top'
            valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                                    OR 
                            (level_type='nominal top' -> 'nominal top' is the only level)  
        
        'geopotential height':
            valid level type(s) = 'pressure'.
            valid levels: (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.   
        
        'latent heat net flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)   
        
        
        'lifted index':
            valid level type(s) = 'pressure'.
            valid levels:
                level_type='pressure' (hPa): 500.
        
        
        'mean sea level pressure':
            valid level type(s): 'mean sea level'.
            valid_levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 
        
        'net longwave radiation flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'net shortwave radiation flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'snow level height':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'humidex':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'orography':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'precipitation rate':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'precipitation type':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'pressure':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of blowing snow':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of drizzle':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of freezing drizzle':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of freezing precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of freezing rain':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of ice pellets':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of liquid precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of rain':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of snow squalls':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of snow':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'probability of thunderstorms':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'relative humidity':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 2, 40, 80, 120
        
        'sea ice fraction':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'secondary precipitation type':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'sensible heat net flux':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'showalter index':
            valid level type(s) = 'pressure'.
            valid levels:
                level_type='pressure' (hPa): 500.
        
        'skin temperature':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'sky state':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'snow density':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'snow depth water equivalent':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'snow depth':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'soil temperature':
            valid level type(s): 'surface', 'depth below surface'.
            valid_levels:
                level_type='depth below surface' (cm):
                    layers=[0, 10] -> 0cm to 10cm below the surface.
                    
                level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
        
        'soil volumetric ice content':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
                
        
        'specific humidity':
            valid level type(s) = 'pressure', 'height above ground', 'surface'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 2, 40, 80, 120
                
                level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
        
        'storm relative helicity':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'surface runoff':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'sweat index':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'temperature':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 2, 40, 80, 120
                
        
        'thickness':
            valid level type(s): 'pressure layer'.
            valid_levels:
                level_type='pressure layer' (hPa):
                    layers=[1000, 500] -> 1000mb to 500mb layer.
                    layers=[850, 700] -> 850mb to 700mb layer. 
                    layers=[1000, 850] -> 1000mb to 850mb layer. 
        
        
        'total cloud cover':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'total precipitation intensity index':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'total precipitation':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        
        'upward longwave radiation flux':
            valid level type(s): 'nominal top'
            valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)
        
        
        'upward shortwave radiation flux':
            valid level type(s): 'nominal top'
            valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)
        
        
        'uv index':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'uv index (clear sky)':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'ventilation index':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'vertical wind shear':
            valid level type(s): 'eta'
            valid levels: None (level_type='eta' -> 'eta' is the only level) 
        
        'vertical velocity':
            valid level type(s): 'pressure'
            valid levels: 
                level_type='pressure' (hPa): 1000, 850, 700, 500, 250
        
        'visibility through ice fog':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'visibility through liquid fog':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'land sea mask':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'wind chill':
            valid level type(s): 'surface'
            valid levels: None (level_type='surface' -> 'surface' is the only level)
        
        'wind direction':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 10, 40, 80, 120
        
        'wind gust':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 10, 40, 80, 120
        
        'wind speed':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 10, 40, 80, 120
        
        'u-wind component':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 10, 40, 80, 120
        
        'v-wind component':
            valid level type(s) = 'pressure', 'height above ground'.
            valid levels:
                level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                    350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                    
                level_type='height above ground' (m): 10, 40, 80, 120   
                
                
    -l = Level. The pressure level in hPa or height above ground in meters.
                    
    Default=500 hPa
          
    -la = Layer. Default=[1000, 500]. 
          
        For level types that correspond to a layer (i.e. 'pressure layer' & 'depth below surface')
        here is where you define the layer. Layers are in the following format for each level_type:
        
        level_type='pressure layer': -> layer=[lower level, upper level] (i.e. layer=[1000, 500] for 1000mb to 500mb layer).
        
        level_type='depth below surface': -> layer=[upper level, lower level] (i.e. layer=[0, 10] for 0cm to 10cm below the surface).          
        
    -lt = Level Type. Type of level (i.e. pressure, height above ground etc.). 
        
        Default='pressure'.
        
        ***Level Types***
    
        'pressure'
        
        'height above ground'
        
        'potential vorticity surface'
        
        'pressure layer'
        
        'depth below surface'
        
        'surface'
        
        'mean sea level'
        
        'nominal top'
        
        'entire atmosphere'
        
        'eta'
        
    --process This flag when set to True will process the data in addition to downloading the data. (Default=True)
    
    --proxy = Proxy Server (Default=None).
    
    Client assumes user is not trying to download data through a proxy server.
    
    If you are using a proxy server you can define it by using --proxy https://proxy-server-address:proxy-server-port
    
    --netcdf = Converts GRIB data into netCDF4 and saves a netCDF (.nc) file. (Default=False). Set to True to create netCDF files.
    
    ***Additional Relevant Flags when --netcdf True***
    
    --ncdir = Defines the local directory where the netCDF (.nc) file saves to. (Default=HRDPS/NETCDF). 
    
    --ncfname = Defines the filename for the netCDF (.nc) file. (Default=hrdps.nc)
    
    ***Complex Example***
    
    1) Download the latest HRDPS for 2-meter temperature 
     
    - Use a proxy server of address: https://proxy-server-address:proxy-server-port 
                        
    2) Create a netCDF (.nc) file of the data called `hrdps_t2m.nc` saved at Weather_Data/HRDPS/NETCDF.
    
    Linux Shell:
        ```wxdata-hrdps fetch latest -lt height_above_ground -l 2 -v temperature \
            --netcdf True --ncdir Weather_Data/HRDPS/NETCDF --ncfname hrdps_t2m.nc \ 
            --proxy https://proxy-server-address:proxy-server-port```
            
    Windows Powershell:
        ```wxdata-hrdps fetch latest -lt height_above_ground -l 2 -v temperature `
            --netcdf True --ncdir Weather_Data/HRDPS/NETCDF --ncfname hrdps_t2m.nc ` 
            --proxy https://proxy-server-address:proxy-server-port```
    
    
    """
@fetch_hrdps_data.command("latest")
@_click.option(
    "--final_forecast_hour",
    "-f",
    default=48,
    show_default=True,
    type=int,
    help="This is the final forecast hour requested in the dataset."
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
    "--custom_directory",
    "-cdir",
    default="none",
    show_default=True,
    type=str,
    help="If you want to save the files in a custom directory - enter the full path here."
)

@_click.option(
    "--clear_data",
    "-cd",
    default=False,
    show_default=True,
    type=bool,
    help="To bypass the safety scanner set --clear data to False."
)


@_click.option(
    "--convert_temperature",
    "-ct",
    default=True,
    show_default=True,
    type=bool,
    help="When set to True any temperature fields are converted from Kelvin to either Celsius or Fahrenheit."
)

@_click.option(
    "--convert_to",
    "-tu",
    default='celsius',
    show_default=True,
    type=str,
    help="When -ct True this is where you declare the units for temperature to be converted to."
)
        
@_click.option('--variable', 
              '-v', 
              default='geopotential_height',
              type=str,
              help=(
                  """Variable to pass into the function. 
                  
                  Default='geopotential_height'
                  
                    ***Variables & Proper level_type & level***
                
                    Any area where valid_levels = None -> Users do not need to edit the optional argument `level`
                    
                    'air density':
                        valid level type(s) = 'height above ground', 'surface'.
                        valid levels:
                            level_type='height above ground' (m): 40, 80, 120 
                            
                            level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
                    
                    
                    'absolute vorticity':
                        valid level type(s): 'pressure'
                        valid levels: 
                            level_type='pressure' (hPa): 1000, 850, 700, 500, 250
                    
                    
                    'albedo':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'blowing snow':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'boundary layer height':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'cape':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'character of precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'cloud water':
                        valid level type(s): 'entire atmosphere'
                        valid levels: None (level_type='entire atmosphere' -> 'entire atmosphere' is the only level)  
                    
                    
                    'conditional freezing precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'conditional amount of liquid precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'conditional amount of solid ice pellets':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'conditional amount of solid snow':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'conditional precipitation rate':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'convective precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'dew point depression':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 2, 40, 80, 120
                    
                    
                    'dew point':
                        valid level type(s) = 'height above ground', 'surface'.
                        valid levels:                      
                            level_type='height above ground' (m): 2, 40, 80, 120
                            
                            level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
                    
                    
                    'dominant precipitation type':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'downward longwave radiation flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'downward shortwave radiation flux':
                        valid level type(s): 'surface', 'nominal top'
                        valid levels: None (level_type='surface' -> 'surface' is the only level) 
                                                                OR 
                                        (level_type='nominal top' -> 'nominal top' is the only level)  
                    
                    'geopotential height':
                        valid level type(s) = 'pressure'.
                        valid levels: (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.   
                    
                    'latent heat net flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)   
                    
                    
                    'lifted index':
                        valid level type(s) = 'pressure'.
                        valid levels:
                            level_type='pressure' (hPa): 500.
                    
                    
                    'mean sea level pressure':
                        valid level type(s): 'mean sea level'.
                        valid_levels: None (level_type='mean sea level' -> 'mean sea level' is the only level) 
                    
                    'net longwave radiation flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'net shortwave radiation flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'snow level height':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'humidex':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'orography':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'precipitation rate':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'precipitation type':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'pressure':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of blowing snow':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of drizzle':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of freezing drizzle':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of freezing precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of freezing rain':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of ice pellets':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of liquid precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of rain':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of snow squalls':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of snow':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'probability of thunderstorms':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'relative humidity':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 2, 40, 80, 120
                    
                    'sea ice fraction':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'secondary precipitation type':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'sensible heat net flux':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'showalter index':
                        valid level type(s) = 'pressure'.
                        valid levels:
                            level_type='pressure' (hPa): 500.
                    
                    'skin temperature':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'sky state':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'snow density':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'snow depth water equivalent':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'snow depth':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'soil temperature':
                        valid level type(s): 'surface', 'depth below surface'.
                        valid_levels:
                            level_type='depth below surface' (cm):
                                layers=[0, 10] -> 0cm to 10cm below the surface.
                                
                            level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
                    
                    'soil volumetric ice content':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                            
                    
                    'specific humidity':
                        valid level type(s) = 'pressure', 'height above ground', 'surface'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 2, 40, 80, 120
                            
                            level_type='surface': None (level_type='surface' -> 'surface' is the only level) 
                    
                    'storm relative helicity':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'surface runoff':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'sweat index':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'temperature':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 2, 40, 80, 120
                            
                    
                    'thickness':
                        valid level type(s): 'pressure layer'.
                        valid_levels:
                            level_type='pressure layer' (hPa):
                                layers=[1000, 500] -> 1000mb to 500mb layer.
                                layers=[850, 700] -> 850mb to 700mb layer. 
                                layers=[1000, 850] -> 1000mb to 850mb layer. 
                    
                    
                    'total cloud cover':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'total precipitation intensity index':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'total precipitation':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    
                    'upward longwave radiation flux':
                        valid level type(s): 'nominal top'
                        valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)
                    
                    
                    'upward shortwave radiation flux':
                        valid level type(s): 'nominal top'
                        valid levels: None (level_type='nominal top' -> 'nominal top' is the only level)
                    
                    
                    'uv index':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'uv index (clear sky)':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'ventilation index':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'vertical wind shear':
                        valid level type(s): 'eta'
                        valid levels: None (level_type='eta' -> 'eta' is the only level) 
                    
                    'vertical velocity':
                        valid level type(s): 'pressure'
                        valid levels: 
                            level_type='pressure' (hPa): 1000, 850, 700, 500, 250
                    
                    'visibility through ice fog':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'visibility through liquid fog':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'land sea mask':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'wind chill':
                        valid level type(s): 'surface'
                        valid levels: None (level_type='surface' -> 'surface' is the only level)
                    
                    'wind direction':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 10, 40, 80, 120
                    
                    'wind gust':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 10, 40, 80, 120
                    
                    'wind speed':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 10, 40, 80, 120
                    
                    'u-wind component':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 10, 40, 80, 120
                    
                    'v-wind component':
                        valid level type(s) = 'pressure', 'height above ground'.
                        valid levels:
                            level_type='pressure' (hPa): 1015, 1000, 985, 975, 950, 925, 900, 875, 850, 800, 750, 700, 650, 600, 550, 500, 450, 400,
                                                350, 300, 275, 250, 225, 200, 175, 150, 100, 50.
                                                
                            level_type='height above ground' (m): 10, 40, 80, 120 
                  
                  See https://edrewitz.github.io/WxData/HRDPS%20CLI for available variables."""
                  
                  )
)

@_click.option(
    '--level', 
    '-l', 
    default=500,
    type=int,  
    help=("""The pressure level in hPa or height above ground in meters.
                    
          Default=500 hPa
          
          See https://edrewitz.github.io/WxData/HRDPS%20CLI for available levels.
          
          """)
)

@_click.option(
    '--layer', 
    '-la', 
    default=[1000, 500],
    type=int,  
    multiple=True,
    help=("""Default=[1000, 500]. 
          
        For level types that correspond to a layer (i.e. 'pressure layer' & 'depth below surface')
        here is where you define the layer. Layers are in the following format for each level_type:
        
        level_type='pressure layer': -> layer=[lower level, upper level] (i.e. layer=[1000, 500] for 1000mb to 500mb layer).
        
        level_type='depth below surface': -> layer=[upper level, lower level] (i.e. layer=[0, 10] for 0cm to 10cm below the surface).
          
          """)
)

@_click.option(
    '--level_type', 
    '-lt', 
    default="pressure",
    type=str,
    show_default=True,
    help=("""Type of level (i.e. pressure, height above ground etc.). 
        
          Default='pressure'.
          
          ***Level Types***
        
            'pressure'
            
            'height above ground'
            
            'potential vorticity surface'
            
            'pressure layer'
            
            'depth below surface'
            
            'surface'
            
            'mean sea level'
            
            'nominal top'
            
            'entire atmosphere'
            
            'eta'
          
          See https://edrewitz.github.io/WxData/HRDPS%20CLI for available level types.
          
          """)
)

@_click.option(
    "--proxy",
    default=None,
    callback=lambda _, __, v: _parse_proxy(v),
    show_default=True,
    help="Proxy URL (e.g., https://address:port). Default: no proxy.",
)

@_click.option(
    "--process",
    default=True,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will process the data in addition to downloading the data. (Default=True)
          """),
)

@_click.option(
    "--netcdf",
    default=False,
    type=bool,
    show_default=True,
    help=("""This flag when set to True will create a netCDF (.nc) file for all the data ingested from the GRIB files.
          """),
)

@_click.option(
    "--ncdir",
    default=f"HRDPS/NETCDF",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the directory where the netCDF (.nc) file will save to.
          """),
)

@_click.option(
    "--ncfname",
    default=f"hrdps.nc",
    type=str,
    show_default=True,
    help=("""This flag is needed when --netcdf True to define the filename for the netCDF (.nc) file. 
          """),
)

def get_gdps(final_forecast_hour,
             clear_recycle_bin,
             custom_directory,
             clear_data,
             convert_temperature,
             convert_to,
             variable,
             level,
             layer,
             level_type,
             proxy,
             process,
             netcdf,
             ncdir,
             ncfname):
    
    """Downloads Latest HRDPS Data"""
    
    try:
        if custom_directory.lower() == "none":
            custom_directory = None
        else:
            custom_directory = custom_directory
            if current_os == "Windows":
                custom_directory = custom_directory.replace('/', '\\')
            else:
                pass
        
        if netcdf == True:
            if current_os == "Windows":
                ncdir = ncdir.replace('/', '\\')
            else:
                pass
        
        variable = variable.lower()
        variable = variable.replace('_', ' ')
            
        level_type = level_type.replace('_', ' ')
        convert_to = convert_to.lower()
        
        if custom_directory == None:
            path = f"HRDPS"
        else:
            path = custom_directory
        
        _fetch_hrdps(final_forecast_hour=final_forecast_hour,
                    clear_recycle_bin=clear_recycle_bin,
                    path=path,
                    clear_data=clear_data,
                    convert_temperature=convert_temperature,
                    convert_to=convert_to,
                    variable=variable,
                    level=level,
                    layer=layer,
                    level_type=level_type,
                    proxies=proxy,
                    process_data=process,
                    to_netcdf=netcdf,
                    netcdf_path=ncdir,
                    netcdf_filename=ncfname,
                    return_values=False)
        
        if current_os != "Windows":
            _click.echo(f"HRDPS latest download complete, data files saved to {path}")
        else:
            path = path.replace('/', '\\')
            _click.echo(rf"HRDPS latest download complete, data files saved to {path}")
            
    except SystemExit as e:
        _command_error_message('hrdps')
        _sys.exit(1)
            
# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
def main():
    hrdps_data()
    
if __name__ == "__main__":
    main()